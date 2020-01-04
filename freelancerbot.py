from freelancersdk.session import Session
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.projects import (
get_projects, get_project_by_id
)
from freelancersdk.resources.projects.helpers import (
create_get_projects_object, create_get_projects_project_details_object,
create_get_projects_user_details_object
)
from freelancersdk.resources.projects.exceptions import \
ProjectsNotFoundException
from freelancersdk.resources.projects.exceptions import \
ProjectsNotFoundException
from freelancersdk.resources.projects.helpers import (
create_search_projects_filter,
create_get_projects_user_details_object,
create_get_projects_project_details_object,
)

from freelancersdk.resources.users.users import get_users, get_user_by_id
from freelancersdk.resources.users.helpers import (
create_get_users_object, create_get_users_details_object,
)
from freelancersdk.resources.users.exceptions import \
UsersNotFoundException


from freelancersdk.resources.projects import place_project_bid
from freelancersdk.resources.users \
import get_self_user_id
from freelancersdk.exceptions import BidNotPlacedException

import os
import json
import pandas as pd
import time
from time import sleep

def sample_place_project_bid(id_proj,value):

	url = os.environ.get('FLN_URL')
	oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
	project_id = os.environ.get('PROJECT_ID')
	
	session = Session(oauth_token='token, url='https://wwww.freelancer.com')
	my_user_id = get_self_user_id(session)
	bid_data = {
	'project_id': int(id_proj),
	'bidder_id': my_user_id,
	'amount': value,
	'period': 4,
	'milestone_percentage': 100,
	'description': 'descripcion del ofertante',
	}
	try:
		return place_project_bid(session, **bid_data)
	except BidNotPlacedException as e:
		#print(('Error message: %s' % e.message))
		print(('Error code: %s' % e.error_code))
		return None
		
def sample_get_user_by_id(user_id):
	url = os.environ.get('FLN_URL')
	oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
	session = Session(oauth_token='6EYaE1bchMaBVl4MAyQv07erW7MT2a', url='https://wwww.freelancer.com')
	
	try:
		p = get_user_by_id(session, user_id)
	except UserNotFoundException as e:
		print(('Error message: {}'.format(e.message)))
		print(('Server response: {}'.format(e.error_code)))
		return None
	else:
		return p

def clear():
    os.system('clear')
    return
#(['active_prepaid_milestone', 'assisted', 'attachments', 'bid_stats',
       #'bidperiod', 'budget', 'can_post_review', 'currency', 'deleted',
       #'deloitte_details', 'description', 'drive_files', 'enterprise_ids',
       #'featured', 'files', 'from_user_location', 'frontend_project_status',
       #'hidebids', 'hireme', 'hireme_initial_bid', 'hourly_project_info', 'id',
       #'invited_freelancers', 'is_buyer_kyc_required', 'is_escrow_project',
       #'is_seller_kyc_required', 'jobs', 'language', 'local', 'local_details',
       #'location', 'nda_details', 'nda_signatures', 'negotiated',
       #'negotiated_bid', 'nonpublic', 'owner_id', 'pool_ids',
       #'preview_description', 'project_collaborations', 'qualifications',
       #'recommended_freelancers', 'seo_url', 'status', 'sub_status',
       #'submitdate', 'support_sessions', 'time_free_bids_expire',
       #'time_submitted', 'time_updated', 'timeframe', 'title', 'track_ids',
       #'true_location', 'type', 'upgrades', 'urgent', 'user_distance'],
      #dtype='object')
#---------------------P
def sample_get_project_by_id(pro_id):
	url = os.environ.get('FLN_URL')
	oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
	session = Session(oauth_token='6EYaE1bchMaBVl4MAyQv07erW7MT2a', url='https://wwww.freelancer.com')
	
	project_id = pro_id
	project_details = create_get_projects_project_details_object(
	full_description=True
	)
	user_details = create_get_projects_user_details_object(
	basic=True
	)
	
	try:
		p = get_project_by_id(session, project_id, project_details, user_details)
	except ProjectsNotFoundException as e:
		print('Error message: {}'.format(e.message))
		print('Server response: {}'.format(e.error_code))
		return None
	else:
		return p
def sample_search_projects():
	url = os.environ.get('FLN_URL')
	oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
	session = Session(oauth_token='6EYaE1bchMaBVl4MAyQv07erW7MT2a', url='https://wwww.freelancer.com')
	
	query = 'Diseño Web,api,bots,python,cryptocurrencies,python bot'
	search_filter = create_search_projects_filter(or_search_query= True,sort_field='time_updated',)
	
	try:
		p = search_projects(session,query=query,search_filter=search_filter,limit=13)
	
	except ProjectsNotFoundException as e:
		print('Error message: {}'.format(e.message))
		print('Server response: {}'.format(e.error_code))
		return None
	else:
		return p

if __name__ == "__main__":
	while True:
		p = sample_search_projects()
		if p:
			#print('Found projects: {}'.format(p))
			#print(p['projects'])
			crypto_df= p['projects']
			dat = pd.DataFrame(crypto_df)
			print(dat['bid_stats'])
			count = -1
			print('---------------------Project freelancer Bot-----------------------')
			print('--------------------------------------------')
			for data in crypto_df:
				count = count + 1
				print ('||| Nombre projecto:' + crypto_df[count]['title'] )
				print('id')
				print(int(crypto_df[count]['id']))
				project_id = int(crypto_df[count]['id'])
				print('Bid')
				bid_stats = crypto_df[count]['bid_stats']
				bid_count = bid_stats['bid_count']
				value = bid_stats['bid_avg']
				print('Propuestas :', bid_count)
				print('Promedio de apuestas :', value)
				
				print('----------------------------------------------------------------------------------------')
				q = sample_get_project_by_id(int(crypto_df[count]['id']))
				if q:
					#print('Found a single project: {}'.format(json.dumps(p)))
					print(q['owner']['id'])
					user_id = q['owner']['id']
					print("Informacion del empleador")
					user_info = sample_get_user_by_id(user_id)
					user_status = user_info['status']
					print(user_status['deposit_made'])
					print(user_status['email_verified'])
					print(user_status['profile_complete'])
					print(user_status['payment_verified'])
					
					
					if user_status['email_verified'] == True and bid_count < 6 and bid_count > 0:
						b = sample_place_project_bid(project_id,value)
						if b:
							print(("Bid placed: %s" % b))
	
				time.sleep(10)
				clear()
	
