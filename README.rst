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
+------------------------+---------------------------------+----------------------------------------------------------------+
| Shortcut               | Function                        | Demo                                                           |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **Right Mouse Button** | **Selecting**                   | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Use the right mouse button to   |     <img src="https://i.imgur.com/EVzmMAm.gif" height="256px"> |
|                        | select any strip in the preview |                                                                |
|                        | window. You will not be able to |                                                                |
|                        | move/scale/rotate/crop a strip  |                                                                |
|                        | until you have added a          |                                                                |
|                        | transform strip (see below.)    |                                                                |
|                        | Hold **SHIFT** while selecting  |                                                                |
|                        | to select multiple strips at    |                                                                |
|                        | once. Press **A** to            |                                                                |
|                        | select/deselect all visible     |                                                                |
|                        | strips.                         |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| :kbd:`T`               | **Add Transform**               | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Add a transform modifier to all |     <img src="https://i.imgur.com/1De0waX.gif" height="256px"> |
|                        | selected strips. Any strips     |                                                                |
|                        | with "Image Offset" enabled     |                                                                |
|                        | will transfer it's offset to    |                                                                |
|                        | the transform strip.            |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **G**                  | **Grab**                        | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Freely position selected        |     <img src="https://i.imgur.com/yQCFI0s.gif" height="256px"> |
|                        | transform strips. Hold          |                                                                |
|                        | **SHIFT** for fine movement.    |                                                                |
|                        | Hold **Ctrl** to enable         |                                                                |
|                        | snapping. Press **X** or **Y**  |                                                                |
|                        | to constrain movement to the X  |                                                                |
|                        | or Y axis accordingly.          |                                                                |
|                        |                                 |                                                                |
|                        | Press **ALT** + **G** to        |                                                                |
|                        | position the selected strips in |                                                                |
|                        | the middle of the window.       |                                                                |
|                        |                                 |                                                                |
|                        | Specify exact movement by       |                                                                |
|                        | typing in the axis (X or Y) and |                                                                |
|                        | the value to move.              |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **S**                  | **Scale**                       | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Scale the selected transform    |     <img src="https://i.imgur.com/oAxSEYB.gif" height="256px"> |
|                        | strips. Hold **SHIFT** for fine |                                                                |
|                        | movement. Hold **Ctrl** to      |                                                                |
|                        | scale in increments.            |                                                                |
|                        |                                 |                                                                |
|                        | Press **ALT** + **S** to        |                                                                |
|                        | restore the scale of the        |                                                                |
|                        | selected strips.                |                                                                |
|                        |                                 |                                                                |
|                        | Specify exact scaling by typing |                                                                |
|                        | in the axis (optional) and the  |                                                                |
|                        | value to scale.                 |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **R**                  | **Rotate**                      | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Rotate the selected transform   |     <img src="https://i.imgur.com/SyL2HeA.gif" height="256px"> |
|                        | strips. Hold **SHIFT** for fine |                                                                |
|                        | movement. Hold **Ctrl** to snap |                                                                |
|                        | to every 5 degrees.             |                                                                |
|                        |                                 |                                                                |
|                        | Press **ALT** + **R** to set    |                                                                |
|                        | the rotation of the selected    |                                                                |
|                        | strips to 0 degrees.            |                                                                |
|                        |                                 |                                                                |
|                        | Specify exact rotation by       |                                                                |
|                        | entering in the value to        |                                                                |
|                        | rotate.                         |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **Q**                  | **Adjust Alpha**                | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Adjust the alpha (opacity) of   |     <img src="https://i.imgur.com/PNsjamH.gif" height="256px"> |
|                        | the selected strips.            |                                                                |
|                        | Hold **Ctrl** to round to       |                                                                |
|                        | nearest tenth.                  |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **C**                  | **Crop/Set Crop**               | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Press **C** to open the crop    |     <img src="https://i.imgur.com/k4r2alY.gif" height="256px"> |
|                        | tool on the active transform    |                                                                |
|                        | strip. Press **C** or **Enter** |                                                                |
|                        | to apply the crop. Press        |                                                                |
|                        | **ESC** to close the crop tool  |                                                                |
|                        | without applying the crop.      |                                                                |
|                        |                                 |                                                                |
|                        | Press **ALT** + **C** to remove |                                                                |
|                        | a strip's cropping.             |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **SHIFT** + **C**      | **Autocrop**                    | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Adjust the scene resolution to  |     <img src="https://i.imgur.com/IarxF14.gif" height="256px"> |
|                        | fit all content in the preview  |                                                                |
|                        | window without adjusting strip  |                                                                |
|                        | sizes or scales.                |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **I**                  | **Insert Keyframe**             | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Open the keyframe insertion     |     <img src="https://i.imgur.com/9Cx6XKj.gif" height="256px"> |
|                        | menu. Alternatively, you may    |                                                                |
|                        | enable Automatic Keyframe       |                                                                |
|                        | Insertion.                      |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
| **,** or **.**         | **Change the Pivot Type**       | .. raw:: html                                                  |
|                        |                                 |                                                                |
|                        | Changes how strips are rotated  |     <img src="https://i.imgur.com/3ru1Xl6.gif" height="256px"> |
|                        | and scaled. When the Pivot Type |                                                                |
|                        | is set to "2D Cursor" you may   |                                                                |
|                        | place the cursor with the left  |                                                                |
|                        | mouse button.                   |                                                                |
+------------------------+---------------------------------+----------------------------------------------------------------+
