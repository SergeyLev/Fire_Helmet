import edgetpu.detection.engine


def classify_frame(input_queue, output_queue):
    engine = edgetpu.detection.engine.DetectionEngine(
        'tpu_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    while True:
        #  Check to see if there is a frame in our input queue
        if not input_queue.empty():
            #  Grab the frame from the input queue
            image = input_queue.get()

            results = engine.detect_with_image(image, threshold=0.4,
                                               keep_aspect_ratio=True, relative_coord=False, top_k=10)
            #  Result data
            data_out = []

            if results:
                for obj in results:
                    inference = []
                    box = obj.bounding_box.flatten().tolist()
                    xmin = int(box[0])
                    ymin = int(box[1])
                    xmax = int(box[2])
                    ymax = int(box[3])

                    inference.extend((obj.label_id, obj.score, xmin, ymin, xmax, ymax))
                    data_out.append(inference)
            output_queue.put(data_out)
