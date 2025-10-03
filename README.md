# VideoCutter
一个使用ffmpeg来批量剪切视频的python脚本。可以限制每个输出文件的大小

## 使用方法
下载python并将ffmpeg添加到path(系统环境变量)
在cmd中输入：
```bash
python main.py input_file output_file [-time from xx to xx]/[-size xxg/m/k]
```
实际上并没有做-time这个功能，~~因为我太懒了~~


现存问题：
1、时间计算不够精确，导致最终可能多生成一个空白视频
2、存储占用计算不够精确（因为使用了流复制），导致精确限制到16G以下比较困难，可以在输入参数是将参数改为16282M(≈15.9G)
