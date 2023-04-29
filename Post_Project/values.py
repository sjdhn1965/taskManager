import settings
class dbvalues(): 
    def setValues():
        dbvalues =  {'dbHost': settings.DATABASES['default']['DBHOST'],
                      'dbUsername' : settings.DATABASES['default']['DBUSER'],
                        'dbPassword':  settings.DATABASES['default']['DBPASS'],
                        'dbName': settings.DATABASES['default']['DBNAME']
                        }
        
        return dbvalues
           
           

       