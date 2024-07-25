from PIL import Image
import numpy as np
import argparse
import tqdm

parser = argparse.ArgumentParser(description="[computer graphics assignment i3] generate the texture from the sample source image")


parser.add_argument("source_file", help="Path to the source image file")
parser.add_argument("target_file", help="Path to save the target image file")
parser.add_argument("-W", "--width", default="none", help="Specify the width (default: same as the source file)")
parser.add_argument("-H", "--height", default="none", help="Specify the height (default: same as the source file)")
parser.add_argument("-e", "--save-each-step", action="store_true", help="save image each epoch")
parser.add_argument("-p", "--probability", default="none", help="probability to adopt a patch (default: 1)")
parser.add_argument("-t", "--t-size", default="30", help="patch size (default: 30)")
parser.add_argument("-s", "--steps", default="none", help="number of steps (default: 10)")
args = parser.parse_args()

prob_inputted=True
n_steps_inputted=True

src=args.source_file
src_img= np.array(Image.open(src))
tgt=args.target_file
if args.width=="none":
    args.width=str(src_img.shape[0])
if args.height=="none":
    args.height=str(src_img.shape[1])
if args.probability=="none":
    args.probability="1"
    prob_inputted=False
if args.steps=="none":
    args.steps="10"
    n_steps_inputted=False
save_each_step=args.save_each_step
t_size = int(args.t_size)
n_steps = int(args.steps)
probability=float(args.probability)



src_size=src_img.shape
tgt_size=[int(args.height), int(args.width),3]
tgt_img = np.random.randint(0,255,tgt_size)



def dist(a,b):
    return ((a-b)**2).sum()

probability2 = 1


if probability>1 or probability<0:
    raise Exception("probability must be between 0 and 1")
for step in tqdm.tqdm(range(n_steps)):
    best_patch = -np.ones(tgt_size[:2]+[2])
    #Search Step
    for tx in tqdm.tqdm(range(tgt_size[0]-t_size+1), leave=False):
        for ty in range(tgt_size[1]-t_size+1):
            if np.random.rand()>=probability2: continue
            best=(None, None)
            for sx in range(src_size[0]-t_size+1):
                for sy in range(src_size[1]-t_size+1):
                    if np.random.rand()>=probability: continue
                    score = dist(src_img[sx:sx+t_size,sy:sy+t_size],tgt_img[tx:tx+t_size,ty:ty+t_size])
                    if best[0] is None:
                        best=(score, np.array([sx,sy]))
                    elif best[0]>score:
                        best=(score, np.array([sx,sy]))
            best_patch[tx][ty]=best[1]

    #Mix Step
    for i in tqdm.tqdm(range(tgt_size[0]), leave=False):
        for j in range(tgt_size[1]):
            value = np.zeros([3])
            count = 0
            for tx in range(max(i-t_size+1,0),min(i+1,tgt_size[0]-t_size+1)):
                for ty in range(max(j-t_size+1,0),min(j+1,tgt_size[1]-t_size+1)):
                    ox, oy = i-tx, j-ty
                    sx, sy=map(int, best_patch[tx][ty])
                    if (sx, sy) == (-1, -1):
                        continue
                    value+=src_img[sx+ox][sy+oy]
                    count+=1
            if count!=0:
                tgt_img[i][j] = np.round(value/count)

    if save_each_step:
        tgt_image = Image.fromarray(tgt_img.astype(np.uint8))
        tgt_image.save(tgt)



tgt_image = Image.fromarray(tgt_img.astype(np.uint8))
tgt_image.save(tgt)
        

                




