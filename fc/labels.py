class Labels:
    my_labels = [None] * 20

    def __init__(self):
        labels_file = 'tpu_models/coco_labels.txt'
        #  Read labels from text files to list
        #  Note. Some items removed from the coco_labels txt hence this
        #  Unused labels can be removed even further

        with open(labels_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(maxsplit=1)
            # noinspection PyTypeChecker
            self.my_labels.insert(int(parts[0]), str(parts[1]))
