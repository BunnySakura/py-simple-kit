import cv2
from tqdm import tqdm

import os
import sys


def video_to_images(video_path, output_folder, step=1):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)
    # 确定视频的总帧数
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # 获取视频帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f"Total frames: {total_frames}")
    print(f"Video FPS: {fps}")

    # 创建进度条对象
    progress_bar = tqdm(total=total_frames,
                        desc="Converting video to images",
                        unit=" frame",
                        file=sys.stdout,
                        colour='green')

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取输出的总帧数
    total_output_frames = len(str(total_frames // step))

    # 逐帧读取视频并保存为图像文件
    frame_count = 0
    while frame_count < total_frames:
        # 读取一帧图像
        ret, frame = video.read()
        if not ret:
            break
        else:
            frame_count += 1

        if frame_count % step == 0:
            # 生成输出图像的等长序号和文件名
            file_serial_number = str(frame_count // step).zfill(total_output_frames)
            output_file = f"{output_folder}/frame_{file_serial_number}.jpg"
            # 保存图像文件
            cv2.imwrite(output_file, frame)

        # 更新进度条
        progress_bar.update(1)

    # 关闭视频文件
    video.release()
    progress_bar.close()
    print("Video to images conversion completed.")


if __name__ == "__main__":
    # 调用函数进行视频转换
    video_to_images("test.mp4", "output")
