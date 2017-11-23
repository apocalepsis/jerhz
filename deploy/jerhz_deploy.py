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
logging_filename = "jerhz_deploy_" + strftime("%Y-%m-%d_%H-%M-%S") + ".log"

# :: EMR PROPERTIES ::
emr_name = "emr_boi"
emr_s3_logging_uri = "s3://aws.demos.jerhz/3p/emr/logging/"
emr_instance_count = 2
emr_ec2_key_name = "NVirginia"
emr_keep_job_flow_alive_when_no_steps = True
emr_termination_protected = False
emr_release_label = "emr-5.9.0"
emr_applications = [
    {"Name" : "Hadoop"},
    {"Name" : "Spark"},
    {"Name" : "Hive"},
    {"Name" : "Zeppelin"}
]
emr_subnet_id = "subnet-bce63e83"
emr_master_instance_type = "m3.xlarge"
emr_master_instance_security_group = "sg-6c08881e"
emr_master_instance_additional_security_groups = ["sg-8e1090fc"]
emr_slave_instance_type = "m3.xlarge"
emr_slave_instance_security_group = "sg-1d07876f"
emr_slave_instance_additional_security_groups = ["sg-8e1090fc"]
emr_visible_to_all_users = True
emr_job_flow_role = "EMR_EC2_DefaultRole"
emr_service_role = "EMR_DefaultRole"

# :: R53 PROPERTIES ::
r53_hosted_zone_id = "Z1NTB46Y263HW7"
r53_resource_record_set_name = "awsome.website"

# :: SES PROPERTIES ::
email_from = "falej@amazon.com"
email_to = "alejandro.x.flores@gmail.com"
email_subject = "[BOI] EMR Cluster Deploy Notification"


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

do_create_cluster = False
do_set_dns_to_emr = False
do_send_email_notification = False

def create_cluster():

    response = {
        "status_code" : 0,
        "payload" : None
    }

    emr_client = boto3.client("emr")
    emr_response = None

    try:
        emr_response = emr_client.run_job_flow(
            Name = emr_name,
            LogUri = emr_s3_logging_uri,
            ReleaseLabel = emr_release_label,
            Instances = {
                "MasterInstanceType" : emr_master_instance_type,
                "SlaveInstanceType" : emr_slave_instance_type,
                "InstanceCount" : emr_instance_count,
                "Ec2KeyName" : emr_ec2_key_name,
                "KeepJobFlowAliveWhenNoSteps" : emr_keep_job_flow_alive_when_no_steps,
                "TerminationProtected" : emr_termination_protected,
                "Ec2SubnetId" : emr_subnet_id,
                "EmrManagedMasterSecurityGroup" : emr_master_instance_security_group,
                "EmrManagedSlaveSecurityGroup" : emr_slave_instance_security_group,
                "AdditionalMasterSecurityGroups" : emr_master_instance_additional_security_groups,
                "AdditionalSlaveSecurityGroups" : emr_slave_instance_additional_security_groups
            },
            Applications = emr_applications,
            VisibleToAllUsers = emr_visible_to_all_users,
            JobFlowRole = emr_job_flow_role,
            ServiceRole = emr_service_role
        )
    except Exception as e:
        response["status_code"] = 1
        response["payload"] = e
        logger.error(e)
    else:
        job_flow_id = emr_response["JobFlowId"]
        while True:
            time.sleep(5)
            emr_response = emr_client.describe_cluster(ClusterId = job_flow_id)
            state = emr_response["Cluster"]["Status"]["State"]
            logger.info("EMR Cluster {} is {}".format(job_flow_id,state))
            response["payload"] = emr_response["Cluster"]
            if state == "WAITING":
                break
            if state in ["TERMINATED","TERMINATED_WITH_ERRORS"]:
                response["status_code"] = 1
                break

    return response

def set_dns_to_emr(emr_cluster):

    response = {
        "status_code" : 0,
        "payload" : None
    }

    if emr_cluster:
        m = re.search("^ec2-(\d+)-(\d+)-(\d+)-(\d+).*\.amazonaws\.com$",
            emr_cluster["MasterPublicDnsName"])
        emr_cluster_ip = None
        if m:
            emr_cluster_ip = m.group(1) + "." + m.group(2) + "." + m.group(3) + "." + m.group(4)

        if emr_cluster_ip:
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
                                    "TTL" : 60,
                                    "ResourceRecords" : [
                                        {"Value" : emr_cluster_ip}
                                    ]
                                }
                            }
                        ]
                    }
                )
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

        else:
            response["status_code"] = 1
            response["payload"] = "Unable to retrieve cluster ip"
    else:
        response["status_code"] = 1
        response["payload"] = "No cluster specified"

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

do_create_cluster = True

emr_response = None
if do_create_cluster:
    logger.info(">>> Creating cluster ...")
    emr_response = create_cluster()
    if emr_response["status_code"] == 0:
        logger.info(emr_response)
        do_set_dns_to_emr = True
    else:
        logger.error(emr_response)
    logger.info("<<< Done.")

dns_response = None
if do_set_dns_to_emr:
    logger.info(">>> Setting up DNS ...")
    dns_response = set_dns_to_emr(emr_response["payload"])
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
