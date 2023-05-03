import qrcode
from PIL import Image, ImageDraw, ImageFont
import platform

OS = platform.system() # Windows, Linux

# Open the file and read the string data on each line
file = open('qrcode_contents.txt', 'r')
contents = file.read().splitlines()

# Calculate the size and spacing of QR code images
qr_size = 200  # Each QR code image has a size of 200 x 200 pixels
qr_padding = 40  # The spacing between the QR code images is 40 pixels

# Define the number of QR codes per row and column and the size of the A4 paper
a4_width = 2480 
a4_height = 3508
row_qr_count = (int)(a4_width / (qr_size + qr_padding))  # QR code number per row

# Calculate the size of the canvas
canvas_width = row_qr_count * (qr_size + qr_padding) - qr_padding
canvas_height = -(-len(contents) // row_qr_count) * (qr_size + qr_padding)

# Create a global canvas with a white background
global_canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

# Set font
fontname = 'DejaVuSans.ttf' if OS == 'Linux' else 'arial.ttf'
font = ImageFont.truetype(fontname, 48)

# Define variables to control the position of each QR code image
x = 0
y = 0

# Loop through each string in the list
for i, content in enumerate(contents):
    # Create a QRCode object and set properties such as size and margin
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    
    print(i)
    # Add data to the QRCode object and generate the QR code image
    qr.add_data(content)
    qr.make(fit=True)

    # Get the QR code image and adjust its size to qr_size x qr_size pixels
    img_qr = qr.make_image(fill_color='black', back_color='white')
    img_qr = img_qr.resize((qr_size, qr_size), Image.ANTIALIAS)

    # Check if the QR code image would go out of bounds
    if x + qr_size > global_canvas.width:
        # If it goes out of bounds, move to the next row and reset the value of x
        y += qr_size + qr_padding
        x = 0

    if y + qr_size > global_canvas.height:
        # If it goes out of bounds, break out of the loop
        break


    # Add the QR code image to the global canvas
    global_canvas.paste(img_qr, (x, y))

    # Add the string content
    draw = ImageDraw.Draw(global_canvas)
    draw.text((x, y + qr_size - 20), content, font=font, fill='black')

    # Control the position of the images
    if i % row_qr_count == row_qr_count - 1:  # If it reaches the end of a row, move to the next row
        x = 0
        y += qr_size + qr_padding + 10
    else:  # Otherwise, move to the next column
        x += qr_size + qr_padding

# Calculate how many A4 paper sheets are required
canvas_count = -(-global_canvas.height // a4_height)  # Round up the number of canvas needed

# Loop through each A4 canvas
for i in range(canvas_count):
    # Create a new A4 canvas with a white background
    canvas = Image.new('RGB', (a4_width, a4_height), 'white')

    # Set the region of the global canvas to copy onto the current A4 canvas
    paste_x = 0
    paste_y = i * a4_height
    paste_width = global_canvas.width
    paste_height = min(a4_height, global_canvas.height - paste_y)

    # Copy the corresponding region from the global canvas to the current A4 canvas
    canvas.paste(global_canvas.crop((paste_x, paste_y, paste_x + paste_width, paste_y + paste_height)))

    # Save the current A4 canvas as a file
    canvas.save('qrcodes_{}.png'.format(i+1))

