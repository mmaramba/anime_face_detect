import os


pos_dir = "positives"
bg_dir_info = "negatives.txt"
vector_dir = "samples"
num_per_img = 1

total_img = 20000
num_iter = total_img // num_per_img

vec_count = 0
tot = 0

# Iterate through positive source directory
for filename in os.listdir(pos_dir):
    if tot >= num_iter:
        break
    tot += 1
    if filename.endswith(".jpg"):
        path_str = pos_dir + "/" + filename
        curr_vec = "{}/{}.vec".format(vector_dir, vec_count)
        # Call OpenCV createsamples application via OS
        os.system("opencv_createsamples -img {} -bg {} -vec {} -num {} -w 48 -h 48".format(
            path_str, bg_dir_info, curr_vec, num_per_img
        ))
        vec_count += 1
    else:
        continue