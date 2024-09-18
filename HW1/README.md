Here's the instructions for this homework: To run my solution, execute the python script with the .raw file in the same directory, requires matplotlib, it should look like this

<img width="586" alt="Screenshot 2024-09-17 at 11 04 45 PM" src="https://github.com/user-attachments/assets/6556f503-6f4e-4d4b-b1e0-6ee11ea60928">

GPU Programming for Video Games
Summer 2024
Homework #1: DIY 3-D Rendering
Due: Friday, June 7, 8:00 PM (via Canvas)
The homework will be graded out of 100 points. If you are unable to complete the assignment by the deadline, turn in what you have for partial credit and move on to the next assignment. Don't forget to include screenshots whether you finished or not -- seeing your screenshots will give me a sense of what to look for when deciding partial credit.

Read these instructions completely and carefully before beginning your work, and do not leave it until the last minute. This is the most challenging homework of the semester.

Using a high-level scripting language of your choice, write a program that implements the geometry transformations and lighting calculations discussed in Lectures 2 through 8 to render an image of a scene consisting of a single 3-D object. For this assignment, you shouldn't worry too much about "modularity," "reuse," "extensibility," "good taste," etc., and you shouldn't worry at all about speed. This is a "quick and dirty" assignment that is primarily intended to make you review the 3-D graphics material we covered and make sure you understand it. 3-D APIs like Direct3D, OpenGL, XNA, and Monogame, and game engines like Unity and Unreal, handle most of this "behind the scenes," but we want to make sure you understand what is going on behind the scenes. Also, you wind up coding much of this "behind the scenes" work explicitly when you write vertex shaders in languages such as HLSL/Cg; hence, there is value in first testing your understanding of these basic computer graphics concepts using a simple language like MATLAB or Python before we add the additional complexities of shader languages on top of it.

Your lighting model should only include a diffuse component arising from a single non-directional point light source. You do not need to include any ambient, emissive, or specular components. You do not need to apply any decay-with-distance type of effects or spotlight effects as described in Lecture 7.

At the top of your program, you should set variables that determine:

The world-space XYZ position of the light source. (We will assume the light color is "unity white," i.e. red, green, and blue = 1, so we won't actually worry about the light color in the calculations.)
The world-space XYZ position of the camera and the XYZ point the camera is looking at.
The world-space position and orientation of the object. There are numerous ways to represent object orientation; we will represent it as rotations around the x, y, and z axis (in that order), with the amount of rotation expressed in degrees. Remember to do the rotations first, then the translation; these operations can all be combined into a signal matrix through matrix multiplication. (FYI, other common orientation representations include pitch, roll, and yaw, and orientation around a specified axis, and the closely related idea of quaternions.) For this assignment, we'll generally be using Direct3D conventions, so you can snag rotation and translation matrices from Microsoft's documentation.
The "field of view" and the "near" and "far" distances of the perspective projection viewing frustum. You may assume an aspect ratio of one.
The RGB color of the diffuse material reflectance of the object, denoted M_diff in the lecture slides. We will assume this is uniform over the entire object.
When we run your code, we should be able to change the variables at the top to render different scenes. The variables should be given easily understandable names.

The first time we ran this course, the students were required to find their own 3-D model and figure out how to read it in. This turned out to be pretty challenging. This year, we are going to let you have benefit of using some of the models that some students in previous years converted to a "raw triangle" format: shark, Download shark,mew, Download mew, mewtwo Download mewtwo,  chief, Download chief,eiffel Download eiffel. Download eiffTo give credit to where it is due, the first three were converted by Arnaud Golinvaux, and the last two were converted by Luke Panayioto. Pick one that you like. The Master Chief and Eiffel Tower models are pretty big files, so you might want to start testing with a smaller file. The files consist of rows of 9 numbers, which are just the x,y,z coordinates of the three vertices of the triangles. You may use one of these model for your assignment, or if you are feeling ambitious, you may find and use a model not given here if you can figure out how to read it in.

In this assignment, we will generally use the Direct3D/XNA convention of representing spatial coordinates as row vectors (vs. OpenGL and Unity, which uses column vectors).

Your program will need to transform each of the vertices of the model by first applying the "world" transformation to get it at the appropriate position and orientation in world coordinates, then applying the "view" transformation to get it into eyespace coordinates, and then applying the "projection" transformation to get it into normalized coordinates. Your program will then divide the x, y, and z coordinates by the w coordinate to implement the perspective effect.

In this assignment, you can pre-multiply the view and projection matrices if you want to save computation time. (You can't premultiply the world transformation matrix too, since you'll need that intermediate result to do the lighting calculations, which we will do in the world space for this assignment.)

Note that since you will be representing coordinates with row vectors, you could store all the vertex coordinates for the object in a single array with number-of-vertex rows and four columns. Then you can multiply that big matrix a 4x4 geometry transformation matrix to transform all of the vertices at once.

You may choose to use a left-handed or right-handed coordinate system; please describe your choice in a comment at the top of your program. You should use the View transformation matrices given in D3DXMatrixLookAtRH or D3DXMatrixLookAtLH. (use (0,1,0) for the "Up" vector), and the perspective transformation matrices given in D3DXMatrixPerspectiveFovLH or D3DXMatrixPerspectiveFovRH. On those pages, "normal" is short for "normalize," "cross" indicates "cross product," and "dot" indicates "dot product." Note that we're just borrowing the equations from the Microsoft documentation; you should write the code to create these various matrices yourself.

For this assignment, use a "flat shading" lighting model. For your lighting calculations, have your program compute its own normal for each flat-faced triangle based on the vertex information for that triangle (instead of using artist-supplied normals for each vertex, as described in class). Most 3D  model files use a left-handed winding convention, so want to compute the normal direction with something like cross(v2 - v1, v3 - v1); if everything looks to dark try negating that (and don't forget to normalize in the lighting calculation). For issues such as computing light vector needed for diffuse light calculations, use the center point of the facet (the average position of the three vertices). In general, lighting calculations can be done in whatever coordinate space you want (object, world, or view/eye), as long as you are consistent. Here, we will do lighting calculations in world coordinates, i.e. do the lighting calculations after you've transformed the object to world coordinates, but before you've transformed them to view coordinates. (Many 3-D engines actually do the lighting in view space, so they can multiply world and view transformation matrices to gain some efficiency. But that involves transforming the lighting positions and pointing vectors as well, and I don't want to make this assignment more complicated than it already is.)

Once you get things into "normalized coordinates," i.e. "clip-space," you only need to worry about "clipping in z," i.e. have your program delete all facets for which one of the z-values of its vertices falls outside the viewing frustum in the z-dimension. Since you will be clipping in z after applying the projective transformation matrix, this is relatively easy since the z values get mapped to a range from 0 to 1 (using the Direct3D conventions). We'll let the scripting language's native triangle drawing features worry about clipping in x and y.

Instead of using a z-buffer to handle the fact that some facets will obscure other facets, use "z-sorting," which is also called the painter's algorithm. Z-sorting was popular when memory was expensive; for instance, the Playstation 1 uses z-sorting. Real-time implementations typically use some sophisticated data structures to do the sorting; here, you can just use the "sort" command built into whatever scripting language you use. After you've done the perspective division operation, compute the average of the z-values of the vertices of each triangle, and sort the facets according to these z-value averages. Then, render the facets in order of farthest to closest.

Choice of implementation language: You should choose a scripting language that has built-in matrix and vector operations (preferably with built-in dot product and cross product operations), as well as a mechanism to draw filled 2-D triangles on the screen - we will let the language handle the rasterization process for you. The language you choose may have built in 3-D graphics features, but you should not use them for this assignment!!!

We recommend using MATLAB; it has all the operations you need "out of the box," including dot and cross products; you can compute many dot and cross products at once with a single line of code. It should be available on most campus lab machines, such as the library and CoC and ECE computing labs. As a Georgia Tech student, you can also get a free license for your own machine. (You also may be able to get some use out of octave, which is mostly MATLAB compatible, or a fantastic new language called Julia, which is MATLABish, keeping the great parts of MATLAB while jettisoning the terrible parts, but not really directly compatible. There is a very nice Julia extension for Visual Studio CodeLinks to an external site.. I actually mostly use Octave instead of MATLAB after years of the MATLAB license server annoying me.) MATLAB's vectorization features let you write compact, expressive code. MATLAB is used throughout the ECE curriculum, particularly in ECE2026. CS and CM students will have been less likely to be exposed to it; however, an advanced CS or CM undergraduate, who has had exposure to many different kinds of programming languages, will have little difficulty picking it up. In any case, if you are CS or CM major, you will find MATLAB to be a worthy weapon to add to your arsenal, as it lets you try out a variety of numerical algorithms with a minimal amount of fuss. Here is an example session at a MATLAB prompt that illustrates various features. ECE students will find this familiar; CS and CM students should be able to quickly get a "feel" for the language.

>> % MATLAB comments start with a % sign
>> % type 'help command' into MATLAB to get help on a particular command
>> % 'ones(rows,columns)' generates a rows-by-columns matrix of 1s
>> % * by itself is matrix multiplication, but .* will do elementwise multiplication
>> % a semicolon at the end of a command suppresses output
>> a = ones(3,1) * (9:-2:1)
a =
     9     7     5     3     1
     9     7     5     3     1
     9     7     5     3     1
>> 	b = (11:-2:7)' * ones(1,5)
b =
    11    11    11    11    11
     9     9     9     9     9
     7     7     7     7     7
>> c = a + b
c =
    20    18    16    14    12
    18    16    14    12    10
    16    14    12    10     8
>> d = a * b
??? Error using ==> mtimes
Inner matrix dimensions must agree.
>> d = a .* b
d =
    99    77    55    33    11
    81    63    45    27     9
    63    49    35    21     7	
>> % compute columnwise cross product
>> cross(a,b)
ans = 
-18   -14   -10    -6    -2
 36    28    20    12     4
-18   -14   -10    -6    -2
>> % compute columnwise dot product
>> dot(a,b)
ans =
   243   189   135    81    27
>> 1 / (c + 3)
??? Error using ==> mrdivide
Matrix dimensions must agree.
>> 1 ./ (c + 3)
ans =
    0.0435    0.0476    0.0526    0.0588    0.0667
    0.0476    0.0526    0.0588    0.0667    0.0769
    0.0526    0.0588    0.0667    0.0769    0.0909
>> dude = [1 2 3; 5 6 7; 11 12 29]
dude =
     1     2     3
     5     6     7
    11    12    29
>> inv(dude)
ans =
	   -1.4062    0.3437    0.0625
	    1.0625    0.0625   -0.1250
	    0.0937   -0.1562    0.0625
>> dude(:,2) = [99 100 101]'
dude =
     1    99     3
     5   100     7
    11   101    29
>> dude(1:2,:)
ans =
     1    99     3
     5   100     7
>> % most importantly for this assignment, MATLAB will also draw triangles for you!
>> the image below was created via these commands:
>> axis([-10 10 -10 10])
>> axis square
>> % the first argument to patch consists of x coordinates, the second consists of y
>> coordinates, and the third consists of an RGB triple
>> patch([3 4 6],[-4 -3 -6],[1 0 0])
>> patch([1 5 9],[10 13 14],[0 1 0])
>> patch([-3 -6 -9],[1 2 5],[0 0 1])
>> patch([-1 -3 -5],[-4 -6 -7],[0.25 0.5 0.3])
There's two versions of the "patch" command in MATLAB. One is for drawing 3-D triangles using MATLABs 3-D graphics capabilities. This isn't what you want here. You want to use the "patch" that draws 2-D triangles, since the point of the assignment is to understand how 3-D objects get turned into 2-D graphics presented on a 2-D screen.

Here is an old MATLAB Tutorial by Prof. Ed Kamen and Prof. Bonnie Heck.

You can tell MATLAB to not draw edges on the patches via set(0,'DefaultPatchEdgeColor','none') - thanks to Michael Cook (a student from a previous year) for the tip.

Warning: The "normalize" command in MATLAB doesn't do what you think it does. It does some weird statistics thing. You can normalize a vector by dividing by its "norm."

If you don't want to use MATLAB, you might try Scilab, R, or perhaps something like Python or Ruby with one of their numeric/scientific/graphical extensions; Mathematica or Maple might also be useable. You can even use Scheme or Lisp, if you can find one that will draw triangles. (If you really insist, you can use a compiled language like Java, Processing, C#, or C++, if you can find an appropriate matrix-manipulation and 2-D graphics library and are willing to lose the interactivity arising from using an interpreted language. However, you probably will find that the assignment will take much longer than necessary if you take that route. That said, I have seen some students produce some reasonably compact solutions to this assignment using Processing; it provides a minimum-fuss way of getting the needed graphics functionality out of Java.)

The main reason we are asking you to use a flat shading model instead of Gourard shading is that MATLAB, as far as we can tell, will only do Gourard shading in a "colormap" sort of mode instead of a full RGB sort of mode.

Homogeneous coordinates in the Direct3D style we are using for this assignment are usually represented as row vectors, with operations conducted by doing row * matrix type operations. However, some of the "vectorized" commands in MATLAB, such as cross and dot, work better with coordinates stored along the columns; hence, you may find it useful to use some transposition operations (indicated using a single quote) to flip between row and column representations as needed. Your mileage may vary.

Deliverables: Package everything needed to run your script (3D data file, program, etc.), as well as three example scenes (in any common image format you'd like) created with your program with different parameters to demonstrate its capability, and upload them to Canvas as a zip file or gzipped tar file. Include "HW1" and as much as possible of your full name in the filename, e.g., HW1_Aaron_Lanterman.zip. (The upload procedure should be reasonably self explanatory once you log in to Canvas.) Be sure to finish sufficiently in advance of the deadline that you will be able to work around any troubles Canvas gives you to successfully submit before the deadline. If you have trouble getting Canvas to work, please e-mail your compressed file to lanterma@ece.gatech.edu, with "GPU HW #1" and your full name in the header line; please only use this e-mail submission as a last resort if Canvas isn't working.

Ground rules: You are welcome to discuss high-level implementation issues with your fellow students, but you should avoid actually looking at one another student's code as whole, and under no circumstances should you be copying any portion of another student's code. However, asking another student to focus on a few lines of your code discuss why you are getting a particular kind of error is reasonable. Basically, these "ground rules" are intended to prevent a student from "freeloading" off another student, even accidentally, since they won't get the full yummy nutritional educational goodness out of the assignment if they do.

Assorted notes:

When rasterizing triangles, 0 to 1 color values may need to be scaled to some integer according to whatever the "native" depth of the frame buffer is. This may vary depending on what language and libraries you use.
You may want to first get a sense of the size of the model you're using. In MATLAB, I'd use min() and max() (obviously use whatever equivalent in whatever language you're using) to find the most extreme vertices in the various dimensions - that should give you a sense of where to put the front-back clipping planes if you move it to some location.
I didn't put anything in the assignment that requires you to be able to scale the object, so you don't have to. It's easy to put in if you feel like it, though (remember to do it before the translation).
If your 3-D model is taking ages to load in, you might want to pre-load it - i.e. put in a flag that checks to see if whatever variable you're loading the model in is already filled, and if it is, doesn't bother to load it again. That's a trick I use a lot. In MATLAB, I use the "clear" command to clear a variable and force a reload if I need to.
How should you choose the field of view? It depends on how far out you put the object - further out, smaller field of view, closer in, bigger field of view, to be able to show the whole object. Most FPS games use a FOV of like 70 to 90 degrees; some let you adjust it. Humans have a FOV closer to 180, although our peripheral vision is shoddy -- it mostly detects motion. So when you're playing a FPS, you're essentially playing with tunnel vision.
Notice that we're not worrying about the "viewport transformation" (not to be confused with the view transformation). After the projection matrix is applied and you do the "perspective divide" - i.e. the divide by w (of course that's assuming you are using a perspective projection matrix - an orthographic projection matrix wouldn't do the divide), your x and y coordinates for viewable points should range from -1 to 1. In your program, you may have some outside of that, but we'll rely on the capability of the 2-D graphics routines in your package to clip edges appropriately. The "viewport transform" is the final transform that maps this -1 to 1 coordinate system into actual pixel coordinates for the screen. Usually the upper left corner is (0,0) in screen pixel coordinates, and the lower right is something like (1023,767). In clip coordinates, y-up is positive, so you usually need to a negation somewhere in there. Anyway, once you figure out what you're mapping to where, it's pretty easy to come up with the mapping you would need; if the display is happening in a particular subset of the screen, i.e. a window you've created, you would need an additional offset. But nowadays you rarely see any of this, as this final Viewpoint Transform is almost always handled by the GPU according to just a few screen size settings in your host API. In MATLAB, you can draw your triangles and then use axis([-1 1 -1 1]) and that will crop the image to those limits. If you're using some other language you might have to do something a bit more complicated. If you'd like to learn more about viewpoint transformations, see here..
There's no reason to assume all your *final* 2-D x and y values will be between -1 and 1; some may be outside the display, which is fine. We're using the drawing capabilities of your language to handle that.
After the perspective transformation, the x and y limits of what you show should be -1 and 1. In MATLAB this can be implemented with "axis([-1 1 -1 1])" followed by "axis square." If you don't set the axis properly, the image will look squished one way or the other.
I've seen some cases where a model looks mostly right but there are a few quirks, like a few random black spots -- I think some of the models may have issues that combine with the problems with the painter's algorithm (it can lead to paradoxes) that show up if the camera is very very very very very close to the object; if you see a problem like this try pulling the camera out a bit and see if it clears up.
You want to set Z_near and Z_far so that it contains your object -- in practice with a real GPU you want to try to make Z_near as big as you can and Z_far as small as you can so you get higher resolution in your z-buffer, but it's tricky because if you make it too tight then it can chop off parts of objects (like in Goldeneye 007 if you get too close to a someone that's looking away from you it chops off the back of their head).
Common errors:

Make sure you don't accidentally put your camera inside the object!
Don't forget to normalize the vectors used in lighting calculation! (This is a common error.)
A lot of folks get confused about all the different coordinate spaces, and do the calculations in the wrong space, or more often, have problems when they erroneously mix two different spaces in one calculation.
In most API convetions, the Z_near and Z_far planes are positive numbers in "worldspace/viewspace length units," even if the coordinate system is right-handed (meaning that Z becomes more negative as objects are moved away from the camera). In the past, I've seen a few cases where someone tried to set Z_near to a negative number (which puts the near plane behind your head) and Z_far to a positive number. That doesn't make sense and will cause things to freak out.
We need Z_near > 0; Z_near = 0 breaks the derivation of the projection matrix.
Sometime people sort the triangles, but when they loop through the triangles, they use the lighting colors they computed for the unsorted triangles, and you get a crazy scrambled look. If you use [blah, index] = sortrows (same with the other sort commands), the index can be useful here. (But there are a bunch of different ways to code this).
The matrices we are borrowing from the DirectX webpages assume a row-vector system, where you multiply vectors by matrices like this:
new_vector = old_vector * transformation_matrix (row-style-transformation)

OpenGL assumes a column-vector system, where you multiply vectors like this:

new_vector = transformation_matrix * old_vector (column-style-transformation)

In the past, I've seen a few instances of people using the DirectX transformation matrices in the second style. If you want to use a column transformation style, you'd need to use the *transpose* of the matrices given in the DirectX documentation.

In the past, I've seen some severely confused students try to element-wise multiply (x,y,z,w) spatial coordinates with colors (r,g,b,w), yielding (x*r,y*g,z*b,w*z). Please don't do that. How would it make sense to multiply the x coordinate by the amount of red??? It's so nonsensical it causes me physical pain to think about people doing that.

Just to re-emphasize, you should only use the 2-D drawing capabilities of your chosen language. Each year I see people working on their programs and they show me a 3-D MATLAB plot with three axes (x, y, and z) shown, and the student could spin the model around using the mouse. IF YOU HAVE SOMETHING LIKE THAT, YOU HAVE DRASTICALLY MISSED THE POINT OF THE ASSIGNMENT. How many dimensions does your laptop screen have? Two dimensions, yes? If you're using the 3-D plotting capabilities of MATLAB to draw your object, how do you think your laptop is turning those 3-D coordinates into things to plot on your 2-D screen????? HW #1 is about programming that pipeline yourself so you understand how it works. Your HW #1 is all about rendering 3-D objects on a 2-D screen by doing the operations that map 3-D object into 2-D. You should only be using 2-D drawing commands that draw in a 2-D window.
After the perspective projection matrix multiply operation, you have homogeneous coordinates for your vertices:

[x,y,z,w]

To finish the perspective projection, you divide by the fourth coordinate:

[x',y',z',1] = [x/w, y/w, z/w, w/w].

At that point, the primary thing you might use z' - or whatever you call that third coordinate - for is the z-sorting, so triangles that are further away from the camera get drawn first, and things closer to the camera get drawn later.

Your plot commands should only be using x',y' in drawing 2-D triangles on the 2-D plane.

Yeah, I know I'm repeating myself a lot. But this issue comes up every time I teach the class.
