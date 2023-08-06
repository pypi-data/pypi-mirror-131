class Profile:
    '''
    EXAMPLE:

    my = Profile('Viboon')
    my.company = 'GGG'
    my.hobby = ['วาดภาพ','Reading','Sleep']
    my.sport = ['ฟุตบอล','Boxing','Hose']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    my.show_sport()
    
    '''
    def __init__(self,name):
        self.name = name
        self.company = ''
        self.hobby = []
        self.sport = []
        self. art = '''
                    
                              /)  (p
                         .-._((,~~.))_.-,
                          `=.   99   ,='
                            / ,o~~o. p
                           { { .__. } }
                            ) `~~~\' (
                           /`-._  _\.-;
                          /         )  ;
                       ,-X        #   X-.
                  hjw   /   \          /   ;
                      (     )| |  | |(     )
                       \   / | |  | | \   /
                        \_(.-( )--( )-.)_/
                        /_,\ ) /  \ ( /._'
                            /_,\  /._\        
                    '''
    
    def show_email(self):
        if self.company != '':
            print('{}@{}.com'.format(self.name.lower(),self.company))
        else:
            print('{}@gmail.com'.format(self.name.lower()))
    
    def show_myart(self):
        print(self.art)

    def show_hobby(self):
        if len(self.hobby) !=0:
            print('------- my hobby -------')
            for i,h in enumerate(self.hobby,start=1):
                print(i,h)
            print('-------------------------')
        else:
            print('No hobby')
    
    def show_sport(self):
        if len(self.sport) !=0:
            print('------- my sport -------')
            for i,h in enumerate(self.sport,start=1):
                    print(i,h)
            print('-------------------------')
        else:
            print('No sport')



if __name__ == '__main__':
    my = Profile('Viboon')
    my.company = 'GGG'
    my.hobby = ['วาดภาพ','Reading','Sleep']
    my.sport = ['ฟุตบอล','Boxing','Hose']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    my.show_sport()



  