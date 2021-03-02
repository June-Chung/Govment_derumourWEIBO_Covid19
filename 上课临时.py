
def fuc(x):
    if x == 10:
        return (x+1)**2
    elif x > 10:
        return  (x-1)**0.5
    else:
        return x ** 10

def triangle(x):
    for  i in range(1,x+1):
        count = i
        string = ""
        for j in range(i):
            string += '*'
        print(string)

def whilefuc(n):
    count = n
    result = 0
    while count:
        result += (2 * count - 1)
        count -= 1
    return result

def user_password():

    while True:
        x = input("username:\n")
        y = input("password:\n")
        if x == 'shelly' and y == '123456':
            break
        else:
            print('error account or password')

if __name__ =='__main__':
    # x = input("input any number")
    # x = int(x)
    # print(fuc(x))
    # triangle(x)
    # print(whilefuc(x))
    user_password()