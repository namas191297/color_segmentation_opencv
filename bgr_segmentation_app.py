import gradio as gr
from utils import process_bgr_image
# Assuming process_image_with_manual_update is defined somewhere

with gr.Blocks() as app:
    gr.Markdown("# Color Segmentation Tool using BGR Colorspace")
    gr.Markdown("Upload an image see the BGR histogram and adjust the BGR bounds to obtain segmented Image based on the range.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Input Controls")
            image_input = gr.Image(type="numpy", label="Upload Image")
            lower = gr.Slider(minimum=0, maximum=180, label="Pixel Intensity Lower Bound", value=0)
            upper = gr.Slider(minimum=0, maximum=180, label="Pixel Intensity Upper Bound", value=255)
            channel = gr.Radio(["Blue", "Green", "Red"], label="Color Channel for Segmentation", value='Blue')
            update_button = gr.Button("Update", variant="primary")

        with gr.Column():
            gr.Markdown("### Output Visualizations")
            bgr_histogram_display = gr.Image(label='BGR Histogram')
            binary_mask_display = gr.Image(label="Segmentation Output")

    update_button.click(
        process_bgr_image, 
        inputs=[image_input, lower, upper, channel], 
        outputs=[bgr_histogram_display, binary_mask_display]
    )

app.launch()