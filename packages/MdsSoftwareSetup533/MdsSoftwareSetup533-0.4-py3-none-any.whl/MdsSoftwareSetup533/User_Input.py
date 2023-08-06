# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---



def mds_software_setup_function():

    import pandas as pd
    try:
        from MdsSoftwareSetup533.mac import anaconda as mac_conda
        from MdsSoftwareSetup533.mac import vscode as mac_vscode
        from MdsSoftwareSetup533.mac import postgresql as mac_psql
        from MdsSoftwareSetup533.windows import anaconda as win_conda
        from MdsSoftwareSetup533.windows import vscode as win_vscode
        from MdsSoftwareSetup533.windows import postgresql as win_psql
        import sys
    except ImportError:
        print("Import Error \n Please check your import statements")
        return
    
    
    class OsInputError(Exception):
        pass
    class SoftwareInputError(Exception):
        pass
    class SubmenuSelectionError(Exception):
        pass
    def move_ahead():
        print(obj.Installation_Guide())
        try:
            move_ahead_param=int(input("\n Want to know more? \n 1. Description \n 2. Tutorial \n 3. For Both \n 4. Back to Previous menu\n " )) 
        except ValueError:
            print("Please enter an integer")
            move_ahead()
        else:
            if (move_ahead_param==1):
                print(obj.Description())
            elif(move_ahead_param==2):
                print(obj.Tutorial())
            elif(move_ahead_param==3):
                print(obj.Tutorial())
                print(obj.Description())
            elif(move_ahead_param==4):
                pass
            else:
                try:
                    move_ahead_param
                    raise SubmenuSelectionError()
                except SubmenuSelectionError:
                    print("\n Select an integer within the range \n")
                    move_ahead()
        
    while(1):
        try:
            OS=int(input("\n Which Operating do you use? \n Enter 1 for Mac \n 2 for Windows \n 3 Exit \n"))
        except ValueError:
            print("Please enter an integer")


            
        else:
        
            if (OS==1):
                while(1):
                    try:
                        software=int(input("\n Which software do you want to install? \n 1. Anaconda \n 2. VSCode \n 3. PostgreSQL \n 4. Back to OS selection \n "))
                    except ValueError:
                        print("Please enter an integer")
                    else:
                        if(software==1):
                            obj=mac_conda.conda_class("conda","Mac")
                            move_ahead()
                        elif(software==2):
                            obj=mac_vscode.vscode("code","Mac")
                            move_ahead()
                        elif(software==3):
                            obj=mac_psql.postgresql("psql","Mac")
                            move_ahead()
                        elif(software==4):
                            break
                        else:
                            try:
                                software
                                raise SoftwareInputError()
                            except SoftwareInputError:
                                print("\n Select an integer within the range \n")
                                
                            
                        
            
            
            elif(OS==2):
                while(1):
                    try:
                        software=int(input("\n Which software do you want to install? \n 1. Anaconda \n 2. VSCode \n 3. PostgreSQL \n 4. Back to OS selection \n"))
                    except ValueError:
                        print("Please enter an integer")
                    else:
                        if(software==1):
                            obj=win_conda.conda_class("conda","Windows")
                            move_ahead()
                        elif(software==2):
                            obj=win_vscode.vscode("code","Windows")
                            move_ahead()
                        elif(software==3):
                            obj=win_psql.postgresql("psql","Windows")
                            move_ahead()
                        elif(software==4):
                            break
                        else:
                            try:
                                software
                                raise SoftwareInputError()
                            except SoftwareInputError:
                                print("\n Select an integer within the range \n")
            elif(OS==3):
                break;
            
            else:
                try:
                    OS
                    raise OsInputError()
                except OsInputError:
                    print("Select an integer within the range")

        



