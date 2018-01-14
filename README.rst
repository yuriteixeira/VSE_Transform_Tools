==================
VSE Transform Tool
==================

.. contents::

Installation
============
1. Download the repository. (click the green button above that says
   "Clone or Download")
2. Open Blender_.
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded .zip file and
   install.
5. Check the box next to "VSE_Transform_Tools"
6. Save User Settings so the addon remains active every time you open
   Blender_

.. _Blender: https://www.blender.org

Usage
=====
+--------------------+---------------------------------+--------------------------------------------+
| Shortcut           | Function                        | Demo                                       |
+--------------------+---------------------------------+--------------------------------------------+
| Right Mouse Button | **Selecting**                   | .. image:: https://i.imgur.com/EVzmMAm.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Use the right mouse button to   |                                            |
|                    | select any strip in the preview |                                            |
|                    | window. You will not be able to |                                            |
|                    | move/scale/rotate/crop a strip  |                                            |
|                    | until you have added a          |                                            |
|                    | transform strip (see below.)    |                                            |
|                    | Hold **SHIFT** while selecting  |                                            |
|                    | to select multiple strips at    |                                            |
|                    | once. Press **A** to            |                                            |
|                    | select/deselect all visible     |                                            |
|                    | strips.                         |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **T**              | **Add Transform**               | .. image:: https://i.imgur.com/1De0waX.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Add a transform modifier to all |                                            |
|                    | selected strips. Any strips     |                                            |
|                    | with "Image Offset" enabled     |                                            |
|                    | will transfer it's offset to    |                                            |
|                    | the transform strip.            |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **G**              | **Grab**                        | .. image:: https://i.imgur.com/yQCFI0s.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Freely position selected        |                                            |
|                    | transform strips. Hold          |                                            |
|                    | **SHIFT** for fine movement.    |                                            |
|                    | Hold **CTRL** to enable         |                                            |
|                    | snapping. Press **X** or **Y**  |                                            |
|                    | to constrain movement to the X  |                                            |
|                    | or Y axis accordingly.          |                                            |
|                    |                                 |                                            |
|                    | Press **ALT** + **G** to        |                                            |
|                    | position the selected strips in |                                            |
|                    | the middle of the window.       |                                            |
|                    |                                 |                                            |
|                    | Specify exact movement by       |                                            |
|                    | typing in the axis (X or Y) and |                                            |
|                    | the value to move.              |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **S**              | **Scale**                       | .. image:: https://i.imgur.com/oAxSEYB.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Scale the selected transform    |                                            |
|                    | strips. Hold **SHIFT** for fine |                                            |
|                    | movement. Hold **CTRL** to      |                                            |
|                    | scale in increments.            |                                            |
|                    |                                 |                                            |
|                    | Press **ALT** to restore the    |                                            |
|                    | scale of the selected strips.   |                                            |
|                    |                                 |                                            |
|                    | Specify exact scaling by typing |                                            |
|                    | in the axis (optional) and the  |                                            |
|                    | value to scale.                 |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **R**              | **Rotate**                      | .. image:: https://i.imgur.com/SyL2HeA.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Rotate the selected transform   |                                            |
|                    | strips. Hold **SHIFT** for fine |                                            |
|                    | movement. Hold **CTRL** to snap |                                            |
|                    | to every 5 degrees.             |                                            |
|                    |                                 |                                            |
|                    | Press <kbc>ALT** to set the     |                                            |
|                    | rotation of the selected strips |                                            |
|                    | to 0 degrees.                   |                                            |
|                    |                                 |                                            |
|                    | Specify exact rotation by       |                                            |
|                    | entering in the value to        |                                            |
|                    | rotate.                         |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **Q**              | **Adjust Alpha**                | .. image:: https://i.imgur.com/PNsjamH.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Adjust the alpha (opacity) of   |                                            |
|                    | the active transform strip.     |                                            |
|                    | Hold **CTRL** to round to       |                                            |
|                    | nearest tenth.                  |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **C**              | **Crop/Set Crop**               | .. image:: https://i.imgur.com/k4r2alY.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Press **C** to open the crop    |                                            |
|                    | tool on the active transform    |                                            |
|                    | strip. Press **C** or **Enter** |                                            |
|                    | to apply the crop. Press        |                                            |
|                    | **Esc** to close the crop tool  |                                            |
|                    | without applying the crop.      |                                            |
|                    |                                 |                                            |
|                    | Press **ALT** to remove a       |                                            |
|                    | strip's cropping.               |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **SHIFT** + **C**  | **Autocrop**                    | .. image:: https://i.imgur.com/IarxF14.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Adjust the scene resolution to  |                                            |
|                    | fit all content in the preview  |                                            |
|                    | window without adjusting strip  |                                            |
|                    | sizes or scales.                |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **I**              | **Insert Keyframe**             | .. image:: https://i.imgur.com/9Cx6XKj.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Open the keyframe insertion     |                                            |
|                    | menu. ALTernatively, you may    |                                            |
|                    | enable Automatic Keyframe       |                                            |
|                    | Insertion.                      |                                            |
+--------------------+---------------------------------+--------------------------------------------+
| **,** or **.**     | **Change the Pivot Type**       | .. image:: https://i.imgur.com/3ru1Xl6.gif |
|                    |                                 |     :width: 256 px                         |
|                    | Changes how strips are rotated  |                                            |
|                    | and scaled. When the Pivot Type |                                            |
|                    | is set to "2D Cursor" you may   |                                            |
|                    | place the cursor with the left  |                                            |
|                    | mouse button.                   |                                            |
+--------------------+---------------------------------+--------------------------------------------+
