import gradio as gr
from utils import process_hsv_image

with gr.Blocks() as app:
    gr.Markdown("# Color Segmentation Tool using HSV Colorspace")
    gr.Markdown("Upload an image see the HSV histogram and adjust the Hue bounds to obtain segmented Image based on the range.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Input Controls")
            image_input = gr.Image(type="numpy", label="Upload Image") 
            lower = gr.Slider(minimum=0, maximum=180, label="Lower Bound Hue Value", value=0)
            upper = gr.Slider(minimum=0, maximum=180, label="Upper Bound Hue Value", value=180)
            update_button = gr.Button("Update", variant="primary")

        with gr.Column():
            gr.Markdown("### Output Visualizations")
            hsv_histogram_display = gr.Image(label='HSV Histogram')
            binary_mask_display = gr.Image(label="Segmentation Output")

    update_button.click(
        process_hsv_image, 
        inputs=[image_input, lower, upper], 
        outputs=[hsv_histogram_display, binary_mask_display]
    )

app.launch()