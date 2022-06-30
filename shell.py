import basic
f = open(r'D:\CC_assignment\test.txt','r')
text = f.read()
result,result_val,result_pos,error = basic.run('<stdin>', text)
in_err = True
x = 0
errors_list = []
parse_tree = []
# for y in range(len(result)):
#     print(result[y])
# print(len(result))
def big_4_search():
    global in_err
    global x
    if(x > len(result)-1):
        return None
    while(in_err):
        if str(result[x]) == "PossibleLoopTokens" or str(result[x]) == "Output Tokens" or str(result[x]) == "if else decalrators" :
            break
        x = x +1
    in_err = False
    if str(result[x]) == "PossibleLoopTokens":
        x = x +1 
        while_gen()
    elif str(result[x]) == "Output Tokens":
        x = x + 1
        p_gen()
    elif str(result[x]) == "if else decalrators":
        x = x + 1
        if_gen()
def cond_gen():
    global in_err
    global x
    if str(result[x]) == "Previous variable" and (str(result[x+1]) == "LESS" or str(result[x+1]) == "GREATER") and str(result[x+2]) == "Previous variable":
        x = x + 3
        print("reduce conditional statement found")
    else :
        # print(result[x])
        # print(result[x+1])
        # print(result[x+2])
        print("wrong declaration of Conditional statement")
        in_err = True
def p_gen():
    global in_err
    global x
    if (str(result[x]) == "LPAREN") and (str(result[x+1]) == "string") and (str(result[x+2]) == "RPAREN") and (str(result[x+3]) == "AST"):
        x = x+4
        print("reduce print stament")
        big_4_search()
    else :
        print("wrong declaration of print statemnet")
        in_err = True
        big_4_search()
def if_gen():
    global in_err
    global x
    # print("reached here")
    if str(result[x]) == "LPAREN":
        # print("reached here")
        x = x + 1
        cond_gen()
        if in_err:
            print("wrong condition in if")
            x = x + 1
            big_4_search()
            return None
    else:
        print("wrong declaraion of if statement")
        in_err = True
        big_4_search()
        return None
    if str(result[x]) == "RPAREN" and str(result[x+1]) == "LFLOW":
        x = x + 2
        big_4_search()
        if str(result[x]) == "RFLOW":
            print("reduce if statment")
            x = x + 1
            big_4_search()
        else:
            in_err = False
            print("if statement did not end well")
            big_4_search()
    else:
        in_err = False
        print("if statement did not end well")
        big_4_search()
def while_gen():
    global in_err
    global x
    if str(result[x]) != "LPAREN" :
        in_err = True
        print("L Paren missing")
        x = x + 1
        big_4_search()
        return None
    else:
        x = x + 1
        cond_gen()
        if(in_err):
            big_4_search()
            return None
    if  str(result[x]) == "RPAREN" and str(result[x+1]) == "LFLOW":
        x = x + 2
        big_4_search()
        if str(result[x]) == "RFLOW":
            print("while loop ")
            x = x + 1
            big_4_search()
        else:
            print("R FLow missing")
            in_err = True
            big_4_search()
    else:
        print("R Paren missing")
        in_err = True
        big_4_search()
big_4_search()
print("kohli")





