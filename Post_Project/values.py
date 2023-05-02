from Post_Project.settings import DATABASES 
class dbvalues(): 
    def setValues():
        dbvalues =  {'dbHost': DATABASES['default']['HOST'],
                      'dbUsername' : DATABASES['default']['USER'],
                        'dbPassword':  DATABASES['default']['PASSWORD'],
                        'dbName': DATABASES['default']['NAME'],
                        'dbPort': DATABASES['default']['PORT']
                        }
        
        return dbvalues
           
           

       