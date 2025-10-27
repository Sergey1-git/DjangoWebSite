from django.shortcuts import render


dict_object_basket = {}

class Basket:
    def __init__(self, id):
        self.id_object=id
        self.args={}


    def add_flower_basket(id, *args):
        #print(type(args[0]))
        #print(type(args[1]))
        print('Вход add_flower_basket ',id, *args)
        if len(args)==2:
            if args[0] not in dict_object_basket[id].args:
                dict_object_basket[id].args[args[0]]=args[1]
            else:
                dict_object_basket[id].args[args[0]]+=1


    def delete_basket_and_form(id):
        del dict_object_basket[id]



def object_basket(id_user, *args):
    print('вход object_basket', id_user, *args)
    flag = True
    if len(dict_object_basket)>0:
        for  key in dict_object_basket:
           if dict_object_basket[key].id_object==id_user:
               flag = False
    if flag:
        dict_object_basket[id_user]=Basket(id_user)
        Basket.add_flower_basket(id_user, *args)
    else:
        Basket.add_flower_basket(id_user, *args)
