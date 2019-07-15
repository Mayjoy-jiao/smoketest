#---------------------------
#测试权重下发坐标块
#上报点击块（１，１）和（5，5）真实数据分别为3次，下发的坐标块为这２个坐标块附近的概率最大
#Author：张姣娇
#--------------------------

# -*- encoding = utf-8 -*-
import requests

url = 'http://css.yule37.cn/api/v1/click/coordinate?url=http://jiao2.iadmob.com/'
print("第一步：设置url  "+url)
# re= requests.request("GET", url)
# print(re.json())

j01 = 0
j02 = 0
j03 = 0
j04 = 0
j05 = 0
j06 = 0
j07 = 0
j08 = 0
j09 = 0
j010 = 0

j11 = 0
j12 = 0
j13 = 0
j14 = 0
j15 = 0
j16 = 0
j17 = 0
j18 = 0
j19 = 0
j110 = 0

j21 = 0
j22 = 0
j23 = 0
j24 = 0
j25 = 0
j26 = 0
j27 = 0
j28 = 0
j29 = 0
j210 = 0

j31 = 0
j32 = 0
j33 = 0
j34 = 0
j35 = 0
j36 = 0
j37 = 0
j38 = 0
j39 = 0
j310 = 0

j41 = 0
j42 = 0
j43 = 0
j44 = 0
j45 = 0
j46 = 0
j47 = 0
j48 = 0
j49 = 0
j410 = 0

j51 = 0
j52 = 0
j53 = 0
j54 = 0
j55 = 0
j56 = 0
j57 = 0
j58 = 0
j59 = 0
j510 = 0

j61 = 0
j62 = 0
j63 = 0
j64 = 0
j65 = 0
j66 = 0
j67 = 0
j68 = 0
j69 = 0
j610 = 0

j71 = 0
j72 = 0
j73 = 0
j74 = 0
j75 = 0
j76 = 0
j77 = 0
j78 = 0
j79 = 0
j710 = 0

j81 = 0
j82 = 0
j83 = 0
j84 = 0
j85 = 0
j86 = 0
j87 = 0
j88 = 0
j89 = 0
j810 = 0

j91 = 0
j92 = 0
j93 = 0
j94 = 0
j95 = 0
j96 = 0
j97 = 0
j98 = 0
j99 = 0
j910 = 0

j101 = 0
j102 = 0
j103 = 0
j104 = 0
j105 = 0
j106 = 0
j107 = 0
j108 = 0
j109 = 0
j1010 = 0


i=10000
while(i):

     re = requests.request("GET", url)
     print(re.json())
     x = re.json()['data']['coordinate']['x']
     y = re.json()['data']['coordinate']['y']
     print("(x,y) is ",(x,y))
#--------------------------------------------------------------------
     if x==1:
               if y == 1:
                    j11 = j11 + 1
                    print(i,"(1,1) count is ", j11)
                    i = i - 1
               elif y == 2:
                    j12 = j12 + 1
                    print(i,"(1,2) count is ", j12)
                    i = i - 1
               elif y == 3:
                    j13 = j13 + 1
                    print(i,"(1,3) count is ", j13)
                    i = i - 1
               elif y == 4:
                    j14 = j14 + 1
                    print(i,"(1,4) count is ", j14)
                    i = i - 1
               elif y == 5:
                    j15 = j15 + 1
                    print(i,"(1,5) count is ", j15)
                    i = i - 1
               elif y == 6:
                    j16 = j16 + 1
                    print(i,"(1,6) count is ", j16)
                    i = i - 1
               elif y == 7:
                    j17 = j17 + 1
                    print(i,"(1,7) count is ", j17)
                    i = i - 1
               elif y == 8:
                    j18 = j18 + 1
                    print(i,"(1,8) count is ", j18)
                    i = i - 1
               elif y == 9:
                    j19 = j19 + 1
                    print(i,"(1,9) count is ", j19)
                    i = i - 1
               else:
                    j110 = j110 + 1
                    print(i,"(1,10) count is ", j110)
                    i = i - 1
#---------------------------------------------------------------------------------
     if x == 2:

               if y == 1:
                         j21 = j21 + 1
                         print(i,"(2,1) count is ", j21)
                         i = i - 1
               elif y == 2:
                              j22 = j22 + 1
                              print(i,"(2,2) count is ", j22)
                              i = i - 1
               elif y == 3:
                              j23 = j23 + 1
                              print(i,"(2,3) count is ", j23)
                              i = i - 1
               elif y == 4:
                              j24 = j24 + 1
                              print(i,"(2,4) count is ", j24)
                              i = i - 1
               elif y == 5:
                              j25 = j25 + 1
                              print(i,"(2,5) count is ", j25)
                              i = i - 1
               elif y == 6:
                              j26 = j26 + 1
                              print(i,"(2,6) count is ", j26)
                              i = i - 1
               elif y == 7:
                              j27 = j27 + 1
                              print(i,"(2,7) count is ", j27)
                              i = i - 1
               elif y == 8:
                              j28 = j28 + 1
                              print(i,"(2,8) count is ", j28)
                              i = i - 1
               elif y == 9:
                              j29 = j29 + 1
                              print(i,"(2,9) count is ", j29)
                              i = i - 1
               else:
                              j210 = j210 + 1
                              print(i,"(2,10) count is ", j210)
                              i = i - 1

#--------------------------------------------------------------------

     if x==3:
               if y == 1:
                    j31 = j31 + 1
                    print(i,"(3,1) count is ", j31)
                    i = i - 1
               elif y == 2:
                    j32 = j32 + 1
                    print(i,"(3,2) count is ", j32)
                    i = i - 1
               elif y == 3:
                    j33 = j33 + 1
                    print(i,"(3,3) count is ", j33)
                    i = i - 1
               elif y == 4:
                    j34 = j34 + 1
                    print(i,"(3,4) count is ", j34)
                    i = i - 1
               elif y == 5:
                    j35 = j35 + 1
                    print(i,"(3,5) count is ", j35)
                    i = i - 1
               elif y == 6:
                    j36 = j36 + 1
                    print(i,"(3,6) count is ", j36)
                    i = i - 1
               elif y == 7:
                    j37 = j37 + 1
                    print(i,"(3,7) count is ", j37)
                    i = i - 1
               elif y == 8:
                    j38 = j38 + 1
                    print(i,"(3,8) count is ", j38)
                    i = i - 1
               elif y == 9:
                    j39 = j39 + 1
                    print(i,"(3,9) count is ", j39)
                    i = i - 1
               else:
                    j310 = j310 + 1
                    print(i,"(3,10) count is ", j310)
                    i = i - 1
#----------------------------------------------------------------
     if x==4:
               if y == 1:
                    j41 = j41 + 1
                    print(i,"(4,1) count is ", j41)
                    i = i - 1
               elif y == 2:
                    j42 = j42 + 1
                    print(i,"(4,2) count is ", j42)
                    i = i - 1
               elif y == 3:
                    j43 = j43 + 1
                    print(i,"(4,3) count is ", j43)
                    i = i - 1
               elif y == 4:
                    j44 = j44 + 1
                    print(i,"(4,4) count is ", j44)
                    i = i - 1
               elif y == 5:
                    j45 = j45 + 1
                    print(i,"(4,5) count is ", j45)
                    i = i - 1
               elif y == 6:
                    j46 = j46 + 1
                    print(i,"(4,6) count is ", j46)
                    i = i - 1
               elif y == 7:
                    j47 = j47 + 1
                    print(i,"(4,7) count is ", j47)
                    i = i - 1
               elif y == 8:
                    j48 = j48 + 1
                    print(i,"(4,8) count is ", j48)
                    i = i - 1
               elif y == 9:
                    j49 = j49 + 1
                    print(i,"(4,9) count is ", j49)
                    i = i - 1
               else:
                    j410 = j410 + 1
                    print(i,"(4,10) count is ", j410)
                    i = i - 1
#-------------------------------------------------------------
     if x==5:
               if y == 1:
                    j51 = j51 + 1
                    print(i,"(5,1) count is ", j51)
                    i = i - 1
               elif y == 2:
                    j52 = j52 + 1
                    print(i,"(5,2) count is ", j52)
                    i = i - 1
               elif y == 3:
                    j53 = j53 + 1
                    print(i,"(5,3) count is ", j53)
                    i = i - 1
               elif y == 4:
                    j54 = j54 + 1
                    print(i,"(5,4) count is ", j54)
                    i = i - 1
               elif y == 5:
                    j55 = j55 + 1
                    print(i,"(5,5) count is ", j55)
                    i = i - 1
               elif y == 6:
                    j56 = j56 + 1
                    print(i,"(5,6) count is ", j56)
                    i = i - 1
               elif y == 7:
                    j57 = j57 + 1
                    print(i,"(5,7) count is ", j57)
                    i = i - 1
               elif y == 8:
                    j58 = j58 + 1
                    print(i,"(5,8) count is ", j58)
                    i = i - 1
               elif y == 9:
                    j59 = j59 + 1
                    print(i,"(5,9) count is ", j59)
                    i = i - 1
               else:
                    j510 = j510 + 1
                    print(i,"(5,10) count is ", j510)
                    i = i - 1
#------------------------------------------------------------------------
     if x==6:
               if y == 1:
                    j61 = j61 + 1
                    print(i,"(6,1) count is ", j61)
                    i = i - 1
               elif y == 2:
                    j62 = j62 + 1
                    print(i,"(6,2) count is ", j62)
                    i = i - 1
               elif y == 3:
                    j63 = j63 + 1
                    print(i,"(6,3) count is ", j63)
                    i = i - 1
               elif y == 4:
                    j64 = j64 + 1
                    print(i,"(6,4) count is ", j64)
                    i = i - 1
               elif y == 5:
                    j65 = j65 + 1
                    print(i,"(6,5) count is ", j65)
                    i = i - 1
               elif y == 6:
                    j66 = j66 + 1
                    print(i,"(6,6) count is ", j66)
                    i = i - 1
               elif y == 7:
                    j67 = j67 + 1
                    print(i,"(6,7) count is ", j67)
                    i = i - 1
               elif y == 8:
                    j68 = j68 + 1
                    print(i,"(6,8) count is ", j68)
                    i = i - 1
               elif y == 9:
                    j69 = j69 + 1
                    print(i,"(6,9) count is ", j69)
                    i = i - 1
               else:
                    j610 = j610 + 1
                    print(i,"(6,10) count is ", j610)
                    i = i - 1
#------------------------------------------------------------------------
     if x==7:
               if y == 1:
                    j71 = j71 + 1
                    print(i,"(7,1) count is ", j71)
                    i = i - 1
               elif y == 2:
                    j72 = j72 + 1
                    print(i,"(7,2) count is ", j72)
                    i = i - 1
               elif y == 3:
                    j73 = j73 + 1
                    print(i,"(7,3) count is ", j73)
                    i = i - 1
               elif y == 4:
                    j74 = j74 + 1
                    print(i,"(7,4) count is ", j74)
                    i = i - 1
               elif y == 5:
                    j75 = j75 + 1
                    print(i,"(7,5) count is ", j75)
                    i = i - 1
               elif y == 6:
                    j76 = j76 + 1
                    print(i,"(7,6) count is ", j76)
                    i = i - 1
               elif y == 7:
                    j77 = j77 + 1
                    print(i,"(7,7) count is ", j77)
                    i = i - 1
               elif y == 8:
                    j78 = j78 + 1
                    print(i,"(7,8) count is ", j78)
                    i = i - 1
               elif y == 9:
                    j79 = j79 + 1
                    print(i,"(7,9) count is ", j79)
                    i = i - 1
               else:
                    j710 = j710 + 1
                    print(i,"(7,10) count is ", j710)
                    i = i - 1
#--------------------------------------------------------------------------------

     if x==8:
               if y == 1:
                    j81 = j81 + 1
                    print(i,"(8,1) count is ", j81)
                    i = i - 1
               elif y == 2:
                    j82 = j82 + 1
                    print(i,"(8,2) count is ", j82)
                    i = i - 1
               elif y == 3:
                    j83 = j83 + 1
                    print(i,"(8,3) count is ", j83)
                    i = i - 1
               elif y == 4:
                    j84 = j84 + 1
                    print(i,"(8,4) count is ", j84)
                    i = i - 1
               elif y == 5:
                    j85 = j85 + 1
                    print(i,"(8,5) count is ", j85)
                    i = i - 1
               elif y == 6:
                    j86 = j86 + 1
                    print(i,"(8,6) count is ", j86)
                    i = i - 1
               elif y == 7:
                    j87 = j87 + 1
                    print(i,"(8,7) count is ", j87)
                    i = i - 1
               elif y == 8:
                    j88 = j88 + 1
                    print(i,"(8,8) count is ", j88)
                    i = i - 1
               elif y == 9:
                    j89 = j89 + 1
                    print(i,"(8,9) count is ", j89)
                    i = i - 1
               else:
                    j810 = j810 + 1
                    print(i,"(8,10) count is ", j810)
                    i = i - 1
#==============================================================================
     if x==9:
               if y == 1:
                    j91 = j91 + 1
                    print(i,"(9,1) count is ", j91)
                    i = i - 1
               elif y == 2:
                    j92 = j92 + 1
                    print(i,"(9,2) count is ", j92)
                    i = i - 1
               elif y == 3:
                    j93 = j93 + 1
                    print(i,"(9,3) count is ", j93)
                    i = i - 1
               elif y == 4:
                    j94 = j94 + 1
                    print(i,"(9,4) count is ", j94)
                    i = i - 1
               elif y == 5:
                    j95 = j95 + 1
                    print(i,"(9,5) count is ", j95)
                    i = i - 1
               elif y == 6:
                    j96 = j96 + 1
                    print(i,"(9,6) count is ", j96)
                    i = i - 1
               elif y == 7:
                    j97 = j97 + 1
                    print(i,"(9,7) count is ", j97)
                    i = i - 1
               elif y == 8:
                    j98 = j98 + 1
                    print(i,"(9,8) count is ", j98)
                    i = i - 1
               elif y == 9:
                    j99 = j99 + 1
                    print(i,"(9,9) count is ", j99)
                    i = i - 1
               else:
                    j910 = j910 + 1
                    print(i,"(9,10) count is ", j910)
                    i = i - 1
#===================================================================================================

     if x==10:
               if y == 1:
                    j101 = j101 + 1
                    print(i,"(10,1) count is ", j101)
                    i = i - 1
               elif y == 2:
                    j102 = j102 + 1
                    print(i,"(10,2) count is ", j102)
                    i = i - 1
               elif y == 3:
                    j103 = j103 + 1
                    print(i,"(10,3) count is ", j103)
                    i = i - 1
               elif y == 4:
                    j104 = j104 + 1
                    print(i,"(10,4) count is ", j104)
                    i = i - 1
               elif y == 5:
                    j105 = j105 + 1
                    print(i,"(10,5) count is ", j105)
                    i = i - 1
               elif y == 6:
                    j106 = j106 + 1
                    print(i,"(10,6) count is ", j106)
                    i = i - 1
               elif y == 7:
                    j107 = j107 + 1
                    print(i,"(10,7) count is ", j107)
                    i = i - 1
               elif y == 8:
                    j108 = j108 + 1
                    print(i,"(10,8) count is ", j108)
                    i = i - 1
               elif y == 9:
                    j109 = j109 + 1
                    print(i,"(10,9) count is ", j109)
                    i = i - 1
               else:
                    j1010 = j1010 + 1
                    print(i,"(10,10) count is ", j1010)
                    i = i - 1
     print("'j11,j12,j13,j14,j15,j16,j17,j18,j19,j110' count is ", j11, j12, j13, j14, j15, j16, j17, j18, j19,
           j110)
     print("'j21,j22,j23,j24,j25,j26,j27,j28,j29,j210' count is ", j21, j22, j23, j24, j25, j26, j27, j28, j29,
           j210)
     print("'j31,j32,j33,j34,j35,j36,j37,j38,j39,j310' count is ", j31, j32, j33, j34, j35, j36, j37, j38, j39,
           j310)
     print("'j41,j42,j43,j44,j45,j46,j47,j48,j49,j410' count is ", j41, j42, j43, j44, j45, j46, j47, j48, j49,
           j410)
     print("'j51,j52,j53,j54,j55,j56,j57,j58,j59,j510' count is ", j51, j52, j53, j54, j55, j56, j57, j58, j59,
           j510)
     print("'j61,j62,j63,j64,j65,j66,j67,j68,j69,j610' count is ", j61, j62, j63, j64, j65, j66, j67, j68, j69,
           j610)
     print("'j71,j72,j73,j74,j75,j76,j77,j78,j79,j710' count is ", j71, j72, j73, j74, j75, j76, j77, j78, j79,
           j710)
     print("'j81,j82,j83,j84,j85,j86,j87,j88,j89,j810' count is ", j81, j82, j83, j84, j85, j86, j87, j88, j89,
           j810)
     print("'j91,j92,j93,j94,j95,j96,j97,j98,j99,j910' count is ", j91, j92, j93, j94, j95, j96, j97, j98, j99,
           j910)
     print("'j101,j102,j103,j104,j105,j106,j107,j108,j109,j1010'",j101, j102, j103, j104, j105, j106,
           j107, j108, j109, j1010)
