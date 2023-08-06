
### Face Parsing
Genreate face parsing with BiSeNet。
pip install dg_face_parsing
1. parsing_face
2. parsing_faces

### Usage
1. dg_util.face_parsing.parsing_face(input_path, output_path)
*input_img- Image data()PIL.image.
*output_path- File path of output image(string, Blank as default).Opional, if output_path is blank, result image returned as cv2.image. Else, result image saved in output path and True returned.
*Return- Image data || Nones
2. dg_util.face_parsing.parsing_faces(input_folder, output_folder)
*Return- None
*input_folder- File path of input folder(string).
*output_folder- File path of output folder(string).