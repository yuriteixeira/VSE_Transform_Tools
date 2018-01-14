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
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| Shortcut                                                                             | Function                                   | Demo                                       |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/rmb.svg        | **Selecting**                              | .. image:: https://i.imgur.com/EVzmMAm.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Use the right mouse button to              |                                            |
|                                                                                      | select any strip in the preview            |                                            |
|                                                                                      | window. You will not be able to            |                                            |
|                                                                                      | move/scale/rotate/crop a strip             |                                            |
|                                                                                      | until you have added a                     |                                            |
|                                                                                      | transform strip (see below.)               |                                            |
|                                                                                      | Hold :kbd:`SHIFT` while                    |                                            |
|                                                                                      | selecting to select multiple               |                                            |
|                                                                                      | strips at once. Press :kbd:`A`             |                                            |
|                                                                                      | to select/deselect all visible             |                                            |
|                                                                                      | strips.                                    |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/t.svg          | **Add Transform**                          | .. image:: https://i.imgur.com/1De0waX.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Add a transform modifier to all            |                                            |
|                                                                                      | selected strips. Any strips                |                                            |
|                                                                                      | with "Image Offset" enabled                |                                            |
|                                                                                      | will transfer it's offset to               |                                            |
|                                                                                      | the transform strip.                       |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/g.svg          | **Grab**                                   | .. image:: https://i.imgur.com/yQCFI0s.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Freely position selected                   |                                            |
|                                                                                      | transform strips. Hold                     |                                            |
|                                                                                      | :kbd:`SHIFT`` for fine                     |                                            |
|                                                                                      | movement. Hold :kbd:`CTRL` to              |                                            |
|                                                                                      | enable snapping. Press :kbd:`X`            |                                            |
|                                                                                      | or :kbd:`Y` to constrain                   |                                            |
|                                                                                      | movement to the X or Y axis                |                                            |
|                                                                                      | accordingly.                               |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Press :kbd:`ALT` + :kbd:`G` to             |                                            |
|                                                                                      | position the selected strips in            |                                            |
|                                                                                      | the middle of the window.                  |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Specify exact movement by                  |                                            |
|                                                                                      | typing in the axis (X or Y) and            |                                            |
|                                                                                      | the value to move.                         |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/s.svg          | **Scale**                                  | .. image:: https://i.imgur.com/oAxSEYB.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Scale the selected transform               |                                            |
|                                                                                      | strips. Hold :kbd:`SHIFT` for              |                                            |
|                                                                                      | fine movement. Hold :kbd:`CTRL`            |                                            |
|                                                                                      | to scale in increments.                    |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Press :kbd:`ALT` + :kbd:`S` to             |                                            |
|                                                                                      | restore the scale of the                   |                                            |
|                                                                                      | selected strips.                           |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Specify exact scaling by typing            |                                            |
|                                                                                      | in the axis (optional) and the             |                                            |
|                                                                                      | value to scale.                            |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/r.svg          | **Rotate**                                 | .. image:: https://i.imgur.com/SyL2HeA.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Rotate the selected transform              |                                            |
|                                                                                      | strips. Hold :kbd:`SHIFT` for              |                                            |
|                                                                                      | fine movement. Hold :kbd:`CTRL`            |                                            |
|                                                                                      | to snap to every 5 degrees.                |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Press :kbd:`ALT` + :kbd:`R` to             |                                            |
|                                                                                      | set the rotation of the                    |                                            |
|                                                                                      | selected strips to 0 degrees.              |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Specify exact rotation by                  |                                            |
|                                                                                      | entering in the value to                   |                                            |
|                                                                                      | rotate.                                    |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/q.svg          | **Adjust Alpha**                           | .. image:: https://i.imgur.com/PNsjamH.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Adjust the alpha (opacity) of              |                                            |
|                                                                                      | the selected strips. Hold                  |                                            |
|                                                                                      | :kbd:`CTRL` to round to nearest            |                                            |
|                                                                                      | tenth.                                     |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/c.svg          | **Crop/Set Crop**                          | .. image:: https://i.imgur.com/k4r2alY.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Press :kbd:`C` to open the crop            |                                            |
|                                                                                      | tool on the active transform               |                                            |
|                                                                                      | strip. Press :kbd:`C` or                   |                                            |
|                                                                                      | :kbd:`ENTER` to apply the crop.            |                                            |
|                                                                                      | Press :kbd:`ESC` to close the              |                                            |
|                                                                                      | crop tool without applying the             |                                            |
|                                                                                      | crop.                                      |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | Press :kbd:`ALT` + :kbd:`C` to             |                                            |
|                                                                                      | remove a strip's cropping.                 |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/shift.svg      | **Autocrop**                               | .. image:: https://i.imgur.com/IarxF14.gif |
|                                                                                      |                                            |                                            |
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/inter_plus.svg | Adjust the scene resolution to             |                                            |
|                                                                                      | fit all content in the preview             |                                            |
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/c.svg          | window without adjusting strip             |                                            |
|                                                                                      | sizes or scales.                           |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/i.svg          | **Insert Keyframe**                        | .. image:: https://i.imgur.com/9Cx6XKj.gif |
|                                                                                      |                                            |                                            |
|                                                                                      | Open the keyframe insertion                |                                            |
|                                                                                      | menu. Alternatively, you may               |                                            |
|                                                                                      | enable Automatic Keyframe                  |                                            |
|                                                                                      | Insertion.                                 |                                            |
|                                                                                      |                                            |                                            |
|                                                                                      | .. image:: https://i.imgur.com/kFtT1ja.jpg |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/comma.svg      | **Change the Pivot Type**                  | .. image:: https://i.imgur.com/3ru1Xl6.gif |
|                                                                                      |                                            |                                            |
| .. image:: https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/period.svg     | Changes how strips are rotated             |                                            |
|                                                                                      | and scaled. When the Pivot Type            |                                            |
|                                                                                      | is set to "2D Cursor" you may              |                                            |
|                                                                                      | place the cursor with the left             |                                            |
|                                                                                      | mouse button.                              |                                            |
+--------------------------------------------------------------------------------------+--------------------------------------------+--------------------------------------------+
