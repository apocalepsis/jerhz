import sys
import re
import time
import boto3
import logging

from time import strftime

# :: AWS PROPERTIES ::
aws_region = "us-east-1"

# :: LOGGING PROPERTIES ::
logging_dir = "/var/log/jerhz"
logging_filename = "jerhz_undeploy_" + strftime("%Y-%m-%d_%H-%M-%S") + ".log"

# :: EMR PROPERTIES ::
emr_name = "emr_boi"

# :: R53 PROPERTIES ::
r53_hosted_zone_id = "Z1NTB46Y263HW7"
r53_resource_record_set_name = "awsome.website"
r53_resource_record_set_alias_hosted_zone_id = "Z3AQBSTGFYJSTF" #Extracted from http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
r53_resource_record_set_alias_name = "s3-website-us-east-1.amazonaws.com"

# :: SES PROPERTIES ::
email_from = "falej@amazon.com"
email_to = "alejandro.x.flores@gmail.com"
email_subject = "[BOI] EMR Cluster Undeploy Notification"


# :: FUNCTIONS ::

logger = logging.getLogger("jerhz")
logger.setLevel(logging.INFO)

logging_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

logging_file_handler = logging.FileHandler("{}/{}".format(logging_dir,logging_filename))
logging_file_handler.setFormatter(logging_formatter)
logger.addHandler(logging_file_handler)

logging_stdout_handler = logging.StreamHandler(sys.stdout)
logging_stdout_handler.setFormatter(logging_formatter)
logger.addHandler(logging_stdout_handler)

do_terminate_cluster = False
do_set_dns_to_s3 = False
do_send_email_notification = False

def terminate_cluster():

    response = {
        "status_code" : 0,
        "payload" : None
    }

    emr_client = boto3.client("emr")
    emr_response = None

    job_flow_id = None

    try:

        emr_response = emr_client.list_clusters(
            ClusterStates = ["WAITING"]
        )
    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        for emr_cluster in emr_response["Clusters"]:
            if emr_cluster["Name"] == emr_name:
                job_flow_id = emr_cluster["Id"]

    if job_flow_id:

        try:

            emr_client.terminate_job_flows(
                JobFlowIds = [job_flow_id]
            )
        except Exception as e:
            response["status_code"] = 1
            response["payload"] = e
            logger.error(e)
        else:
            while True:
                time.sleep(5)
                emr_response = emr_client.describe_cluster(ClusterId = job_flow_id)
                state = emr_response["Cluster"]["Status"]["State"]
                logger.info("EMR Cluster {} is {}".format(job_flow_id,state))
                response["payload"] = emr_response["Cluster"]
                if state == "TERMINATED":
                    break
                if state == "TERMINATED_WITH_ERRORS":
                    response["status_code"] = 1
                    break

    return response

def set_dns_to_s3():

    response = {
        "status_code" : 0,
        "payload" : None
    }

    r53_client = boto3.client('route53')
    r53_response = None
    try:
        r53_response = r53_client.change_resource_record_sets(
            HostedZoneId = r53_hosted_zone_id,
            ChangeBatch = {
                "Changes" : [
                    {
                        "Action" : "UPSERT",
                        "ResourceRecordSet" : {
                            "Name" : r53_resource_record_set_name,
                            "Type" : "A",
                            "AliasTarget" : {
                                "HostedZoneId" : r53_resource_record_set_alias_hosted_zone_id,
                                "DNSName" : r53_resource_record_set_alias_name,
                                "EvaluateTargetHealth" : False
                            }
                        }
                    },
                    {
                        "Action" : "UPSERT",
                        "ResourceRecordSet" : {
                            "Name" : "www.{}".format(r53_resource_record_set_name),
                            "Type" : "A",
                            "AliasTarget" : {
                                "HostedZoneId" : r53_resource_record_set_alias_hosted_zone_id,
                                "DNSName" : r53_resource_record_set_alias_name,
                                "EvaluateTargetHealth" : False
                            }
                        }
                    }
                ]
            }
        )
        print("R53 RESPONSE: {}".format(r53_response))
    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        change_info = r53_response["ChangeInfo"]
        while True:
            time.sleep(5)
            try:
                r53_response = r53_client.get_change(
                    Id = change_info["Id"]
                )
                status = r53_response["ChangeInfo"]["Status"]
                logger.info("Change Status {} is {}".format(change_info["Id"],status))
                if status == "INSYNC":
                    try:
                        r53_response = r53_client.list_resource_record_sets(
                            HostedZoneId = r53_hosted_zone_id,
                            StartRecordName = r53_resource_record_set_name,
                            StartRecordType = 'A',
                            MaxItems = '1'
                        )
                    except Exception as e:
                        response["status_code"] = 1
                        response["payload"] = e
                        logger.error(e)
                    else:
                        response["payload"] = r53_response["ResourceRecordSets"]
                    break
            except Exception as e:
                response["status_code"] = 1
                response["payload"] = e
                logger.error(e)
                break

    return response

def send_email(body_text,body_html):

    response = {
        "status_code" : 0,
        "payload" : None
    }

    ses_client = boto3.client("ses",region_name = aws_region)

    ses_response = None

    try:

        ses_response = ses_client.send_email(
            Source = email_from,
            Destination = {
                "ToAddresses" : [email_to]
            },
            Message = {
                "Body" : {
                    "Html" : {
                        "Charset" : "utf-8",
                        "Data" : body_html
                    },
                    "Text" : {
                        "Charset" : "utf-8",
                        "Data" : body_text
                    }
                },
                "Subject" : {
                    "Charset" : "utf-8",
                    "Data" : email_subject
                }
            }
        )

    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        response["payload"] = ses_response

    return response

# :: MAIN ::

do_terminate_cluster = True

emr_response = None
if do_terminate_cluster:
    logger.info(">>> Terminating cluster ...")
    emr_response = terminate_cluster()
    if emr_response["status_code"] == 0:
        logger.info(emr_response)
        do_set_dns_to_s3 = True
    else:
        logger.error(emr_response)
    logger.info("<<< Done.")

dns_response = None
if do_set_dns_to_s3:
    logger.info(">>> Setting up DNS ...")
    dns_response = set_dns_to_s3()
    if dns_response["status_code"] == 0:
        logger.info(dns_response)
        do_send_email_notification = True
    else:
        logger.error(dns_response)
    logger.info("<<< Done.")

if do_send_email_notification:
    logger.info(">>> Sending notification email ...")
    email_body_text = "EMR Response:\n{}\n\nR53 Response:\n{}\n\n".format(emr_response,dns_response)
    email_body_html = "EMR Response:<br/>{}<br/><br/>R53 Response:<br/>{}<br/><br/>".format(emr_response,dns_response)
    ses_response = send_email(email_body_text,email_body_html)
    logger.info("<<< Done.")
