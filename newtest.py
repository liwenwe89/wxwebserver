__author__ = 'cherish'
import orderdatabase
if __name__ == '__main__':
    c =orderdatabase.orderdatabase();
    # b = orderdatabase.orderdatabase.getNameFromID(c,"oyePbvjkGXL8VAvtny8MyX4NVX7I")
    b = orderdatabase.orderdatabase.insterOrder(c,"oyePbvjkGXL8VAvtny8MyX4NVX7I",1)
    b = orderdatabase.orderdatabase.insterOrder(c,"CCT1",1)
    b = orderdatabase.orderdatabase.insterOrder(c,"CCT2",1)
    b = orderdatabase.orderdatabase.insterOrder(c,"CCT3",1)
    b = orderdatabase.orderdatabase.insterOrder(c,"CCT4",1)
    b=orderdatabase.orderdatabase.howManyOrderToday(c);
    b = orderdatabase.orderdatabase.insterOrder(c,"CCT1",-1)
    b= orderdatabase.orderdatabase.howManyOrderToday(c);

    print(b)
    print b[0]
    print b[1][0]
    print b[2][0]
    print b[3][b[1][0]]
#    Basic.__init__(Basic)
#    Basic.run(Basic);