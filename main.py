import subprocess
import sys
import os
import json
'''
def validate_video_file(filepath):
    """验证视频文件是否有效"""
    if not os.path.exists(filepath):
        return False
    
    try:
        # 使用 ffprobe 快速验证文件
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", filepath]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.returncode == 0
    except:
        return False
'''

def getVideoExtension(inputFile):
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',           # 只显示错误信息
            '-show_format',           # 显示格式信息
            '-show_streams',          # 显示流信息
            '-print_format', 'json',   # 输出为JSON格式
            inputFile
        ]

        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            format_name = info['format']['format_name']
            detected_formats = [fmt.strip() for fmt in format_name.split(',')]
            format_mapping = {
            'mp4': ['mov', 'mp4', 'm4a', '3gp'],
            'mkv': ['matroska', 'webm'],
            'avi': ['avi'],
            'flv': ['flv'],
            'wav': ['wav']
            }
            status = 0
            print(f"Your input file's extension may be:{detected_formats}")
            for key, value in format_mapping.items():
                for t in value:
                    if value == detected_formats:
                        format_name = key
                        status = 1
                        break
            
            if(status == 0):
                print("Can't find input file's extension.")
                sys.exit(1)
            else:
                return format_name


            
        else:
            print(f"error:{result.stderr}")
    

    except FileNotFoundError:
        print(f"error:Can't find the command 'ffprobe'. Have you installed FFmpeg?")
    except Exception as e:
        print(f"an error occured:{e}")


def getVideoDuration(inputFile):
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            inputFile
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        duration = float(result.stdout.strip())
        return duration
    except subprocess.CalledProcessError as e:
        print(f"error:can't get the video duration.\nffprobe return the information:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print("error:Can't find the command 'ffprobe'. Have you installed FFmpeg?")
        return None
    except ValueError:
        print("error:Can't analyse the value returned from ffmpeg")
        return None




def checkFile(path):
     if os.path.exists(path):
          return True
     else:
          return False




def Cut_Size(inputFile, outputFile, size, extension):
    if(size[len(size) - 1] == 'g' or size[len(size) - 1] == 'G'):
        max_size = float(size[:len(size)-1]) * 1024 * 1024 * 1024
    elif(size[len(size) - 1] == 'm' or size[len(size) - 1] == 'M'):
        max_size = float(size[:len(size)-1]) * 1024 * 1024
    elif(size[len(size) - 1] == 'k' or size[len(size) - 1] == 'K'):
        max_size = float(size[:len(size)-1]) * 1024
    else:
        raise IndexError("input error, please enter 'python main.py -help' for more information.")
    
    print(max_size)

    # 初始化
    part_number = 1
    start_time = 0.0
    input_ = inputFile
    output = f"{outputFile}_part1.{extension}"
    cmd = [
                    'ffmpeg', '-y',
                    '-i', input_,
                    '-ss', str(start_time),
                    '-c', 'copy',
                    '-fs', str(max_size),
                    '-avoid_negative_ts', '1',
                    output
                ]
    

    total_duration = getVideoDuration(inputFile)
    if total_duration is None:
        print("error:Can't get the total duration of the video.")
        sys.exit(1)
    print (total_duration)

    # start




    while start_time < total_duration:
        try:    
            print(f"Generating part {part_number}...\n start time:{start_time}\n output:{output} \n input:{input_}")
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            part_number += 1
            output = f"{outputFile}_part{part_number}.{extension}"
            start_time += getVideoDuration(f"{outputFile}_part{part_number - 1}.{extension}")

            # 更新
            cmd = [
                    'ffmpeg', '-y',
                    '-i', input_,
                    '-ss', str(start_time),
                    '-c', 'copy',
                    '-fs', str(max_size),
                    '-avoid_negative_ts', '1',
                    output
                ]
            
        except subprocess.CalledProcessError as e:
            print(f"error:{e}")
        except:
            print("an unknown error occured.")
            sys.exit(0)






def main():

    # help
    if len(sys.argv) > 1 and sys.argv[1] == '-help':
            print('python main.py input_file output_file [-time from xx to xx]/[-size xxg/m/k]')
            sys.exit(0)
    try:    
        if(len(sys.argv) < 5):
             raise IndexError("input error, please enter 'python main.py -help' for more information.")
        
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]

        if not checkFile(inputFile):
            raise IOError("Input file not find, please check your input.")
        
        if checkFile(outputFile):
            print("The output file name is already in use.Are you SURE to continue? Y/N")
            temp = input()
            if temp == 'Y' or temp == 'y':
                pass
            else:
                 raise IOError("User abandoned the operation.")
        
        #extension
        extension = (getVideoExtension(inputFile))

        
        if(sys.argv[3] == '-time'):
            pass
        elif(sys.argv[3] == '-size'):
            Cut_Size(inputFile, outputFile, sys.argv[4], extension)
        


            
    except IndexError as e:
        print(f"error:{e}")
    except Exception as e:
        print(f"error:{e}")
    except IOError as e:
        print(f"error:{e}")


if __name__ == '__main__':
    main()