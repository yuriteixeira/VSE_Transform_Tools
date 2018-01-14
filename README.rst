===================
VSE_Transform_Tools
===================

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
+------------------------+-----------------------------------+--------------------------------------------+
| Shortcut               | Function                          | Demo                                       |
+------------------------+-----------------------------------+--------------------------------------------+
| **Right Mouse Button** | **Selecting**                     | .. image:: https://i.imgur.com/EVzmMAm.gif |
|                        |                                   |                                            |
|                        | Use the right mouse button to     |                                            |
|                        | select any strip in the preview   |                                            |
|                        | window. You will not be able to   |                                            |
|                        | move/scale/rotate/crop a strip    |                                            |
|                        | until you have added a            |                                            |
|                        | transform strip (see below.)      |                                            |
|                        | Hold **Shift** while selecting    |                                            |
|                        | to select multiple strips at      |                                            |
|                        | once. Press **A** to              |                                            |
|                        | select/deselect all visible       |                                            |
|                        | strips.                           |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **T**                  | **Add Transform**                 | .. image:: https://i.imgur.com/1De0waX.gif |
|                        |                                   |                                            |
|                        | Add a transform modifier to all   |                                            |
|                        | selected strips. Any strips       |                                            |
|                        | with "Image Offset" enabled       |                                            |
|                        | will transfer it's offset to      |                                            |
|                        | the transform strip.              |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **G**                  | **Grab**                          | .. image:: https://i.imgur.com/yQCFI0s.gif |
|                        |                                   |                                            |
|                        | Freely position selected          |                                            |
|                        | transform strips. Hold            |                                            |
|                        | **Shift** for fine movement.      |                                            |
|                        | Hold **Ctrl** to enable           |                                            |
|                        | snapping. Press **X** or **Y**    |                                            |
|                        | to constrain movement to the X    |                                            |
|                        | or Y axis accordingly.            |                                            |
|                        |                                   |                                            |
|                        | Press **Alt** + **G** to          |                                            |
|                        | position the selected strips in   |                                            |
|                        | the middle of the window.         |                                            |
|                        |                                   |                                            |
|                        | Specify exact movement by         |                                            |
|                        | typing in the axis (X or Y) and   |                                            |
|                        | the value to move.                |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **S**                  | **Scale**                         | .. image:: https://i.imgur.com/oAxSEYB.gif |
|                        |                                   |                                            |
|                        | Scale the selected transform      |                                            |
|                        | strips. Hold **Shift** for fine   |                                            |
|                        | movement. Hold **Ctrl** to        |                                            |
|                        | scale in increments.              |                                            |
|                        |                                   |                                            |
|                        | Press **Alt** to restore the      |                                            |
|                        | scale of the selected strips.     |                                            |
|                        |                                   |                                            |
|                        | Specify exact scaling by typing   |                                            |
|                        | in the axis (optional) and the    |                                            |
|                        | value to scale.                   |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **R**                  | **Rotate**                        | .. image:: https://i.imgur.com/SyL2HeA.gif |
|                        |                                   |                                            |
|                        | Rotate the selected transform     |                                            |
|                        | strips. Hold **Shift** for fine   |                                            |
|                        | movement. Hold **Ctrl** to snap   |                                            |
|                        | to every 5 degrees.               |                                            |
|                        |                                   |                                            |
|                        | Press <kbc>Alt** to set the       |                                            |
|                        | rotation of the selected strips   |                                            |
|                        | to 0 degrees.                     |                                            |
|                        |                                   |                                            |
|                        | Specify exact rotation by         |                                            |
|                        | entering in the value to          |                                            |
|                        | rotate.                           |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **Q**                  | **Adjust Alpha**                  | .. image:: https://i.imgur.com/PNsjamH.gif |
|                        |                                   |                                            |
|                        | Adjust the alpha (opacity) of     |                                            |
|                        | the active transform strip.       |                                            |
|                        | Hold **Ctrl** to round to         |                                            |
|                        | nearest tenth.                    |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **C**                  | **Crop/Set Crop**                 | .. image:: https://i.imgur.com/k4r2alY.gif |
|                        |                                   |                                            |
|                        | Press **C** to open the crop      |                                            |
|                        | tool on the active transform      |                                            |
|                        | strip. Press **C** or **Enter**   |                                            |
|                        | to apply the crop. Press          |                                            |
|                        | **Esc** to close the crop tool    |                                            |
|                        | without applying the crop.        |                                            |
|                        |                                   |                                            |
|                        | Press **Alt** + **C** to remove a |                                            |
|                        | strip's cropping.                 |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **Shift** + **C**      | **Autocrop**                      | .. image:: https://i.imgur.com/IarxF14.gif |
|                        |                                   |                                            |
|                        | Adjust the scene resolution to    |                                            |
|                        | fit all content in the preview    |                                            |
|                        | window without adjusting strip    |                                            |
|                        | sizes or scales.                  |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **I**                  | **Insert Keyframe**               | .. image:: https://i.imgur.com/9Cx6XKj.gif |
|                        |                                   |                                            |
|                        | Open the keyframe insertion       |                                            |
|                        | menu. Alternatively, you may      |                                            |
|                        | enable Automatic Keyframe         |                                            |
|                        | Insertion.                        |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
| **,** or **.**         | **Change the Pivot Type**         | .. image:: https://i.imgur.com/3ru1Xl6.gif |
|                        |                                   |                                            |
|                        | Changes how strips are rotated    |                                            |
|                        | and scaled. When the Pivot Type   |                                            |
|                        | is set to "2D Cursor" you may     |                                            |
|                        | place the cursor with the left    |                                            |
|                        | mouse button.                     |                                            |
+------------------------+-----------------------------------+--------------------------------------------+
