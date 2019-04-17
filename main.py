from boto3.session import Session
from datetime import datetime, timedelta
import pytz

''' cluster lifetime limit in hours '''
LIMIT = 2
''' your local timezone '''
TIMEZONE = 'Europe/Berlin'

AWS_ACCESS_KEY = 'AKIA3IEKS2VZEFV6QAXB'
AWS_SECRET_KEY = 'lnUrJOjBKYCR5p65UHBMtW5Zr7jiQ28DOeOwdGEV'
AWS_REGION = 'eu-west-1'

print('Start cluster check')

emrsession = Session(AWS_ACCESS_KEY, AWS_SECRET_KEY)
emr = emrsession.client('emr', AWS_REGION)

local_tz = pytz.timezone(TIMEZONE)
today = local_tz.localize(datetime.today(), is_dst=None)
lifetimelimit = today - timedelta(hours=LIMIT)

clusters = emr.list_clusters(
    CreatedBefore=lifetimelimit,
    ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING', 'TERMINATING']
)

if clusters['Clusters'] is not None:
    for cluster in clusters['Clusters']:
        print('Terminating Cluster: %s active since: %s' % (cluster['Id'], cluster['Status']['Timeline']['CreationDateTime']))
        emr.terminate_job_flows(
            JobFlowIds=[cluster['Id']]
        )

print('cluster check done')
