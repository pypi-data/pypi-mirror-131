#!/usr/bin/python
class Var:
      nameA='exe.py'  #nameA!  
      nameB=2.11  #nameB! 
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
        

          if  name!=None and vvv!=None:
              #######################################################
            #   with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
            #         ############################
            #         f.seek(0,0)       ## 規0
            #         R =f.readlines( ) 
            #         R[1]=f"      nameA='{name}'\n"
            #         R[2]=f"      nameB='{vvv}'\n"
            #         ##########################
            #         f.seek(0,0)       ## 規0
            #         f.writelines(R)
                            
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                

                                    

                    # N="name"
                    NR=["#nameA!","#nameB!"]
                    ######## 禁止i.strip() 刪除 \n 和\tab ############
                    ### R is ########## 本檔案 #######################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    # R=[ i for i in open(__file__).readlines()] 
                    # print(R)

                    ###############
                    # Q=[ (ii,i) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in ["#nameA!","#nameB!"]   ]
                    Q=[ (i,b) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in NR   ]
                    # print(Q)

                    if len(Q)==len(NR):
                        # print("**Q",*Q)
                        NR=[ i.strip("#!") for i in NR] ## 清除[#!] ---> ["nameA","nameB"]
                        NG=[ f"'{name}'" , vvv ]
                        def RQQ( i , b ):
                            # print( "!!",i ,b)
                            NRR = NR.pop(0) 
                            NGG = NG.pop(0) 
                            import re
                            # print(Q[0]) ## (2, 'nameA=None  #nameA!')
                            R01 = list(  b  )     ## 字元陣列 ## 

                            N01 = "".join(R01).find( f"{ NRR }")
                            R01.insert(N01,"=")
                            # print( R01  )

                            N01 = "".join(R01).find( f"#{ NRR }!")
                            R01.insert(N01,"=")
                            # print( R01  )

                            ### 修改!.
                            QQA="".join(R01).split("=")
                            QQA.pop(2)
                            QQA.insert(2, f"={ NGG }  ")
                            # print("!!QQA","".join(QQA)  )

                            ### 本檔案..修改
                            return  i ,"".join(QQA)

                        for ar in Q:
                            # print("!XXXX")
                            N,V = RQQ( *ar )
                            R[N] = V
                        ##########################
                        f.seek(0,0)       ## 規0
                        # print("@ R ",R)
                        f.writelines(R)


              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  # print( NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




# ################################################################################################
# def siteOP():
#     import os,re
#     pip=os.popen("pip show pip")
#     return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 

# ## 檢查 ln 狀態
# !ls -al { siteOP()+"/cmds" }


            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            # 'echo >/content/cmd.py/cmds/__init__.py',
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: Moon@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
          for i in cls.text:
              cls.popen(i)
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)


class init(Var):
    #   classmethod
    #   def 
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= cls.dir
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
                                  
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
          else:
                print("警告: 參數或型別 出現問題") 


# class sdist(MD,PIP,init):

class sdist(MD,PIP):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"

      @classmethod
      def rm(cls):
          import os
          # /content/sample_data   
          if os.path.isdir("/content/sample_data"):
            os.system(f"rm -rf /content/sample_data")



            ################################################################################ 
          if not os.path.isfile("/content/True"):
            ################################################################################  
            if os.path.isdir("dist"):
                print("@刪除 ./dist")
                ##### os.system(f"rm -rf ./dist")
                print( f"rm -rf {os.getcwd()}{os.path.sep}dist" )
                os.system(f"rm -rf {os.getcwd()}{os.path.sep}dist")
            ##
            info = [i for i in os.listdir() if i.endswith("egg-info")]
            if  len(info)==1:
                if os.path.isdir( info[0] ):
                    print(f"@刪除 ./{info}")
                    #  os.system(f"rm -rf ./{info[0]}")
                    os.system(f"rm -rf {os.getcwd()}{os.path.sep}{info[0]}")
            ################################################################################

      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          import os
          print("!XXXXX:" ,os.getcwd() )
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          ################################


          ######## 刪除
          cls.rm()      
          ##############################################################
        #   CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist bdist_wheel"
          CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist --formats=zip"
          # CMDtxt = cls.popen(CMD)
          ## print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@[set]@@@@@\n",CMDtxt)
          ################################################################
          

          print("@ 目前的 pwd :",os.getcwd() ,not os.path.isfile("/content/True") )


          ##  !twine 上傳
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = f"twine upload --skip-existing  {os.getcwd()}{os.path.sep}dist{os.path.sep}*"
              # print("@222@",cls.popen(CMD))

              #  if not os.path.isfile("/content/True"): ## [True]
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)
          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    # os.system("python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                   
                    ## 結束 ##
                    BLFF="結束."

                
        
          
          ######## 刪除
          cls.rm()     
          ###################   
          return  this
          


### 首次---參數輸入
################################################# 這裡是??????      
import sys
if    len(sys.argv)==3 :
    ##########################
    ## 產生:設定黨
    if sys.argv[2].find(r"--formats=zip") == -1:
        Var(sys.argv[1],sys.argv[2])
        ################################################
        import os
        sdist(os.path.dirname(sys.argv[0]))






###########################################!????
# from pip._internal.cli.main import *
###################################################
import os,sys
# 會建立這兩個
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-pip-egg-info
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'bdist_wheel', '-d', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-wheel-l_q1vm4y']
# print("@ 建立tmp ::",sys.argv)
###############################################



import sys
# if 'egg_info' in sys.argv: 
#     print("!!XX")
if 'bdist_wheel' in sys.argv:

    nameA= f"{Var.nameA}" 
    nameB= f"{Var.nameB}"  
    ############################## 只有一次 
    import re,os.path as P 
    R=re.findall(f"##\[{nameA}\].*##\[{nameA}\]",open(P.__file__,"r").read(),re.S)
    ##############
    if len(R)==0:
        def showPIP():
            import os,re
            pip=os.popen("pip show pip")
            # return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
            nameQP = re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
            return nameQP + os.path.sep + nameA+ r"-" +nameB+ r".dist-info" 
        text='''
##['''+nameA+''']

# def job(nameA,nameB):
#     print("pip uninstall !!")
#     # from pip._internal.cli.main import *
#     # main(["uninstall",nameA,"-y"])
#     ###########################################################################################
#     def showPIP():
#         return r"'''+ showPIP() +'''" 
#     ## 如果不存在
#     ## SH.py-11.44.dist-info
#     import os
#     nameQ = showPIP() + os.path.sep + nameA+ r"-" +nameB+ r".dist-info" 
#     print("@ nameQ :",nameQ)
#     ### 刪除
#     ###########################################################################################
#     import os
#     while True:
#         if os.path.isdir(nameQ):
#             break
#     if os.name=="posix":     ## Linux系統
#         os.system(f"rm -rf {nameQ}")
#     elif os.name=="nt":     ## Win10系統
#         os.system(f"rmdir /q /s {nameQ}")
#     ############################################################################################
#     ############################################################################################
    
# def  fun():
#     print("123456!!")
#     # import os
#     # os.system(f"pip uninstall '''+nameA+''' -y")
#     job("'''+nameA+'","'+nameB+'''")


import sys
if 'bdist_wheel' in sys.argv:
    def  cleanup_function( **dictOP ):   
        print("!!!!!!!!!!!!!!!!!!!!!結束")
        # fun()
        ##########################
        import re
        R=re.findall("##\['''+nameA+'''\].*##\['''+nameA+'''\]",open(__file__,"r").read(),re.S)
        S="".join(open(__file__,"r").read().split(R[0]))
        ## del
        open(__file__,"w").write(S)
        ########################### 


    import site , atexit
    atexit.register(cleanup_function, siteOP= site)
##['''+nameA+''']
'''
        # import os.path as P
        # open(P.__file__,"a+").write(text) ## 寫入
        # import importlib as L
        # L.reload( P ) ## 更新



if   sdist.VVV and (not "BLFF" in dir()):
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean'  or sys.argv[1]== 'build' :





    # import builtins
    # builtins.__dict__["QQA"]=123

    
    ##############################################
    from setuptools.command.install import install
    
    #####
    from subprocess import check_call
    
    
    nameA= f"{Var.nameA}" 
    nameB= f"{Var.nameB}"
    package= f"{sdist.dir}"
     
    

    # import os
    # os.system(f"echo  {os.getpid()} ,{os.getppid() } >/content/PPID999") 

    #### pip-install
    from pip._internal.cli.main import *
    class PostCMD(install):
          """cmdclass={'install': XXCMD,'install': EEECMD }"""
          def  run(self):
              import builtins as B
              B.__dict__["QQ"]="ABC"

              import os
              install.run(self)
              print(nameA,nameB)


          
              ########################## 只有一次 
              import re,pip as PA 
              R=re.findall(f"##\[{nameA}\].*##\[{nameA}\]",open(PA.__file__,"r").read(),re.S)
              ##############
              if len(R)==0:
                text='''
##['''+nameA+''']
import sys,os
if   "--compile" in sys.argv and "--no-cache-dir" in sys.argv:
    os.system("pip uninstall '''+nameA+''' -Y")
##['''+nameA+''']
'''
                open(PA.__file__,"a+").write(text)
              ##################################
              #nameA="QQP"
              ############################## 只有一次 
              import re,os.path as PB 
              R=re.findall(f"##\[{nameA}\].*##\[{nameA}\]",open(PB.__file__,"r").read(),re.S)
              ##############
              if len(R)==0:
                text='''
##['''+nameA+''']
print("9999")
# def  fun():
#     print("我要刪除東西!!")
# def  cleanup_function( **dictOP ):   
#     fun()
# import site , atexit
# atexit.register(cleanup_function, siteOP= site)

##########################################
import sys
if "'''+nameA+'''" in [i if len(i.split("=="))==1 else i.split("==")[0] for i in sys.argv]:
    ### 如果有
    if "uninstall" in sys.argv:
        ### 清除 os.path  ##[tag標籤]
        ##########################
        import re
        R=re.findall("##\['''+nameA+'''\].*##\['''+nameA+'''\]",open(__file__,"r").read(),re.S)
        S="".join(open(__file__,"r").read().split(R[0]))
        ## del
        open(__file__,"w").write(S)
        ###########################
##['''+nameA+''']
'''
                open(PB.__file__,"a+").write(text) ## 寫入
              else:
                os.system("pip uninstall " +nameA+ " -Y")
                # import importlib as L
                # L.reload( P ) ## 更新



              os.system('start cmd /c "timeout /nobreak /t 3&&python -c "print("123456789")"')

                    


            #   print(" main 暫停 " , os.getpid() ,os.getppid())
            #   os.system(f"echo  {os.getpid()} ,{os.getppid() } >/content/PPID") 
              
            #   import sys
            # #   os.system(f"echo  { sys.argv } >/content/sys") 
            # #   print("@ sys id :",[id(i) for i in sys.argv]  )
            # #   os.system(f"echo  { [id(i) for i in sys.argv] } >/content/sys") 
            #   os.system(f"echo 123>/content/sys") 



            #   import psutil 
            #   ppid = os.getppid()
            #   pp  = psutil.Process( ppid ) 
            # #   pp.suspend() ## 子程序 暫停
            # #   print(" 兒子 還在跑 QQXX  ")
            

             

              print("# 小貓 1 號")
            #   import importlib as L
            #   import sys
            #   sys.path.append("/content")
            #   import builtins as B
            #   B.__dict__["R"] = L.import_module("R")
              def  cleanup_function( PIP , nameA , nameB ):
                    import os
                    # print("# 小貓 2 號",         os.path.isdir(PIP+ os.path.sep + nameA+ r"-" +nameB+ r".dist-info" ) , PIP+ os.path.sep + nameA+ r"-" +nameB+ r".dist-info" )
                    print("# 小貓 2 號")
                    # quit()
                    # import sys
                    # sys.exit()


                    # # import os.path as P
                    # # open(P.__file__,"a+").write(text) ## 寫入
                    # # import importlib as L
                    # # L.reload( P ) ## 更新
                    # ####################################################################
                    # ################################################################### 相同的 PID 程序
                    # import threading
                    # import time

                    # # 子執行緒的工作函數
                    # def job(PIP,nameA,nameB):
                    #     ## 如果不存在
                    #     ## SH.py-11.44.dist-info
                    #     import os
                    #     nameQ = PIP + os.path.sep + nameA+ r"-" +nameB+ r".dist-info" 
                    #     print("@ nameQ :",nameQ)
                    #     ### 刪除
                    #     ###########################################################################################
                    #     import os
                    #     print("@ nameQ :",nameQ , os.path.isdir(nameQ))
                        
                    #     # import time
                    #     # time.sleep(20)
                    #     ## 執行python 關閉cmd控制台
                    #     # os.system('start cmd /k "python -c \"print(123)\""')
                    #     import os
                    #     os.system(r'start cmd /k "timeout /nobreak /t 3&&python -c \"print(123)\""')
                    #     # while True:
                    #     #     print("@ BL: ",os.path.isdir(nameQ) )
                    #     #     if os.path.isdir(nameQ):
                    #     #         pass
                    #     #         # break
                    #     # if os.name=="posix":     ## Linux系統
                    #     #     os.system(f"rm -rf {nameQ}")
                    #     # elif os.name=="nt":     ## Win10系統
                    #     #     os.system(f"rmdir /q /s {nameQ}")
                    #     # ############################################################################################
                    #     # ############################################################################################
                    #     # while True:
                    #     #     import time
                    #     #     time.sleep(5)
                    #     #     os.system(r"echo > C:\QQPXX")
                        
                    
                    # # 建立一個子執行緒
                    # t = threading.Thread(target = job, args=(PIP,nameA,nameB))
                    # import os
                    # # print("@ t.PID::",os.getpid())
                    # ########################
                    # # 執行該子執行緒
                    # t.start()
                    # ############################################################################
                    # ###########################################################################
                    # t.join()
                    # ##########
                    # #########

                    # import os
                    # os.system("pip -V")
                    # # os.system(f"pip uninstall {nameA} -y")
                    
                    # # import sys
                    # # sys.exit()


                    # from multiprocessing import Process, Manager

                    # def job(d):
                    #     ###########################################################################################
                    #     def showPIP():
                    #             import os,re
                    #             pip=os.popen("pip show pip")
                    #             return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
                    #     ## 如果不存在
                    #     ## SH.py-11.44.dist-info
                    #     nameQ = showPIP() + os.path.sep + nameA+ r"-" +nameB+ r".dist-info" 
                    #     print("@ nameQ :",nameQ)
                    #     ### 刪除
                    #     ###########################################################################################
                    #     import os
                    #     while True:
                    #         if os.path.isdir(nameQ):
                    #             break
                    #     if os.name=="posix":     ## Linux系統
                    #         os.system(f"rm -rf {nameQ}")
                    #     elif os.name=="nt":     ## Win10系統
                    #         os.system(f"rmdir /q /s {nameQ}")
                    #     ############################################################################################
                    #     ############################################################################################

                    # # manager = Manager()
                    # # d = manager.dict()
                    # # p1.start()
                    

                    # # 子執行緒的工作函數
                    # # def job(d):
                    

                    # ##################################################### 相同的 PID 程序
                    # import threading
                    # # 建立一個子執行緒
                    # t = threading.Thread(target = job, args=(123,))
                    # t.start()
               
                    
# ########## 取得 [git] PID
# import psutil , os
# pid = os.popen("git config R.pid").read().strip() 
# pp = psutil.Process( int(pid) )   
# # pp.suspend() ## 子程序 暫停 ......... 站亭子程序 但是 子孫不聽話
# pp.resume() ## 繼續跑

              import site, atexit
              atexit.register(cleanup_function, showPIP() , nameA , nameB )
              #################################
                
            

    

            



    ################################################
    # # with open("/content/QQ/README.md", "r") as fh:
    # with open("README.md", "r") as fh:
    #           long_description = fh.read()


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    
    setup(
      
          name  =   f"{Var.nameA}"  ,
        
          version=  f"{Var.nameB}"  ,
      

          author   = "小貓程式",
          description = "[這是一隻程式]",
          author_email = "520@gmial.com" ,
          
          
          #long_description=long_description,
          long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
          long_description_content_type="text/markdown",
    
          license="LGPL",
          
          packages = find_packages(), 
         




        #   ## python 入口點
        #   entry_points={
          
        #         'console_scripts':[                                                        
        #             'cmdsSQL=SQL.databasesB:main',  
        #             'cmdsMD=md.databases:main',                      
        #         ],
        #   },

          ################################
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          }
        #   ,
          #########################
        #   include_package_data=True, # 將數據文件也打包
        #   zip_safe=True
    )
   

### B版
# 6-13