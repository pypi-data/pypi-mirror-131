def cv2_file_extension(encode):
    encode = encode.upper()
    if encode in ['I420', # 该参数是YUV编码类型，文件名后缀为.avi   广泛兼容，但会产生大文件
                  'PIMI', # 该参数是MPEG-1编码类型，文件名后缀为.avi
                  'XVID']: # 该参数是MPEG-4编码类型，文件名后缀为.avi  要限制结果视频的大小，这是一个很好的选择。
        return 'avi'
    elif encode in ['MP4V', 'X264', # MPEG-4编码，文件名后缀为.mp4，想限制结果视频的大小，这可能是最好的选择。
                    'U263', 'I263']: # H2634 可以直接在h5中使用video播放的流式文件编码 codec .mp4
        return 'mp4'