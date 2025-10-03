# VideoCutter
一个使用ffmpeg来批量剪切视频的python脚本。可以限制每个输出文件的大小

## 使用方法
下载python并将ffmpeg添加到path(系统环境变量)
在cmd中输入：
```bash
python main.py input_file output_file [-time from xx to xx]/[-size xxg/m/k]
```
实际上并没有做-time这个功能，~~因为我太懒了~~
