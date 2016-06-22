USERS = {'admin':'123',
			'viewer':'viewer'}
GROUPS = {'admin':['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
