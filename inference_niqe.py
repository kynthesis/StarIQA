import argparse
import glob
import os
from pyiqa import create_metric
from tqdm import tqdm


def main():
    """Inference demo for pyiqa.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default=None, help='input image/folder path.')

    args = parser.parse_args()

    metric_name = 'NIQE'.lower()

    # set up IQA model
    iqa_model = create_metric(metric_name, metric_mode='NR')

    if os.path.isfile(args.input):
        input_paths = [args.input]
    else:
        input_paths = sorted(glob.glob(os.path.join(args.input, '*')))

    avg_score = 0
    test_img_num = len(input_paths)
    pbar = tqdm(total=test_img_num, unit='image')
    for img_path in input_paths:
        score = iqa_model(img_path).cpu().item()
        avg_score += score
        pbar.update(1)
    pbar.close()
    avg_score /= test_img_num
    print(f'NIQE: {round(avg_score, 4)}')


if __name__ == '__main__':
    main()
