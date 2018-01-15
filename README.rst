.. raw:: html

    <h1>VSE_Transform_Tools</h1>
        
    Contents:

    <ul>
        <li>
            <a name="top_installation" href="#installation">Installation</a>
            <ul>
                <li><a name="top_automatic_updating" href="#automatic_updating">Automatic Updating</a></li>
            </ul>
        </li>
        <li>
            <a name="top_usage" href="#usage">Usage</a>
            <ul>
                <li><a name="top_selecting" href="#selecting">Selecting</a></li>
                <li><a name="top_add_transform" href="#add_transform">Add Transform</a></li>
                <li><a name="top_grab" href="#grab">Grab</a></li>
                <li><a name="top_scale" href="#scale">Scale</a></li>
                <li><a name="top_rotate" href="#rotate">Rotate</a></li>
                <li><a name="top_adjust_alpha" href="#adjust_alpha">Adjust Alpha</a></li>
                <li><a name="top_crop" href="#crop">Crop</a></li>
                <li><a name="top_autocrop" href="#autocrop">Autocrop</a></li>
                <li><a name="top_insert_keyframe" href="#insert_keyframe">Insert Keyframe</a></li>
                <li><a name="top_change_pivot_type" href="#change_pivot_type">Change Pivot Type</a></li>
            </ul>
        </li>
    </ul>

    <h2><a name="installation" href="#top_installation">Installation</a></h2>
    <ol>
        <li>Download the repository. (Click the green button above that says "Clone or Download")</li>
        <li>Open Blender</li>
        <li>Go to File &gt; User Preferences &gt; Addons</li>
        <li>Click "Install From File" and navigate to the downloaded .zip file and install.</li>
        <li>Check the box next to "VSE_Transform_Tools"</li>
        <li>Save User Settings so the addon remains active every time you open Blender</li>
    </ol>

    <h3><a name="automatic_updating" href="#top_automatic_updating">Automatic Updating</a></h3>

    <p>
        On installation, you will have the option to make Blender automatically 
        check for addon updates. If "Auto-check for Update" is enabled, then Blender will
        check for an update when the <a href="#add_transform">Add Transform</a> operator 
        is run and the time since the last update check is greater than "interval between 
        checks".
    </p>
    <p>
        If an update is available and "Auto-check for Update" is enabled, a popup will 
        appear offering to install the most recent version. Click outside the box to 
        ignore it, or click OK to install the new version.
    </p>

    <h2><a name="usage" href="#top_usage">Usage</a></h2>
    <table>
        <tr>
            <th>Shortcut</th>
            <th>Function</th>
            <th width="256px">Demo</th>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/rmb.svg" alt="Right Mouse Button">
            </td>
            
            <td>
                <p><b><a name="selecting" href="#top_selecting">Selecting</a></b></p>
                <p>
                    Use the right mouse button to select any strip in the preview window.
                    You will not be able to move/scale/rotate/crop a strip until you have
                    added a transform strip (see below.) Hold <kbd>SHIFT</kbd> while
                    selecting to select multiple strips at once. Press <kbd>A</kbd> to
                    select/deselect all visible strips.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/EVzmMAm.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/t.svg" alt="T">
            </td>
            <td>
                <p><b><a name="add_transform" href="#top_add_transform">Add Transform</a></b></p>
                <p>
                    Add a transform modifier to all selected strips. Any strips with "Image
                    Offset" enabled will transfer it's offset to the transform strip.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/1De0waX.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/g.svg" alt="G">
            </td>
            <td>
                <p><b><a name="grab" href="#top_grab">Grab</a></b></p>
                <p>
                    Freely position selected transform strips. Hold <kbd>SHIFT</kbd> for fine
                    movement. Hold <kbd>CTRL</kbd> to enable snapping. Press <kbd>X</kbd> or
                    <kbd>Y</kbd> to constrain movement to the X or Y axis accordingly.
                </p>
                <p>
                    Press <kbd>ALT</kbd> + <kbd>G</kbd> to position the selected strips in the
                    middle of the window.
                </p>
                <p>
                    Specify exact movement by typing in the axis (X or Y) and the value to
                    move.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/yQCFI0s.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/s.svg" alt="S">
            </td>
            <td>
                <p><b><a name="scale" href="#top_scale">Scale</a></b>
                <p>
                    Scale the selected transform strips. Hold <kbd>SHIFT</kbd> for fine
                    movement. Hold <kbd>CTRL</kbd> to scale in increments.
                </p>
                <p>
                    Press <kbd>ALT</kbd> + <kbd>S</kbd> to restore the scale of the selected
                    strips.
                </p>
                <p>
                    Specify exact scaling by typing in the axis (optional) and the value to
                    scale.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/oAxSEYB.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/r.svg" alt="R">
            </td>
            <td>
                <p><b><a name="rotate" href="#top_rotate">Rotate</a></b>
                <p>
                    Rotate the selected transform strips. Hold <kbd>SHIFT</kbd> for fine
                    movement. Hold <kbd>CTRL</kbd> to snap to every 5 degrees.
                </p>
                <p>
                    Press <kbd>ALT</kbd> + <kbd>R</kbd> to set the rotation of the selected strips
                    to 0 degrees.
                </p>
                <p>
                    Specify exact rotation by entering in the value to rotate.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/SyL2HeA.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/q.svg" alt="Q">
            </td>
            <td>
                <p><b><a name="adjust_alpha" href="#top_adjust_alpha">Adjust Alpha</a></b></p>
                <p>
                    Adjust the alpha (opacity) of the selected strips. Hold <kbd>CTRL</kbd>
                    to round to nearest tenth.
                </p>
                <p>
                    Press <kbd>Alt</kbd>+<kbd>Q</kbd> to set the selected strips' opacity to 1.0
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/PNsjamH.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/c.svg" alt="C">
            </td>
            <td>
                <p><b><a name="crop" href="#top_crop">Crop</a></b></p>
                <p>
                    Press <kbd>C</kbd> to open the crop tool on the active transform strip.
                    Press <kbd>C</kbd> or <kbd>ENTER</kbd> to apply the crop. Press
                    <kbd>ESC</kbd> to close the crop tool without applying the crop.
                </p>
                <p>
                    Press <kbd>ALT</kbd> + <kbd>C</kbd> to remove a strip's cropping.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/k4r2alY.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/shift.svg" alt="SHIFT">
                <br>
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/inter_plus.svg" alt="+">
                <br>
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/c.svg" alt="C">
            </td>
            <td>
                <p><b><a name="autocrop" href="#top_autocrop">Autocrop</a></b></p>
                <p>
                    Adjust the scene resolution to fit all visible content in the preview window
                    without adjusting strip sizes or scales.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/IarxF14.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/i.svg" alt="I">
            </td>
            <td>
                <p><b><a name="insert_keyframe" href="#top_insert_keyframe">Insert Keyframe</a></b></p>
                <p>
                    Open the keyframe insertion menu. Alternatively, you may enable
                    Automatic Keyframe Insertion.
                </p>
                <img src="https://i.imgur.com/kFtT1ja.jpg">
            </td>
            <td>
                <img src="https://i.imgur.com/9Cx6XKj.gif">
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/comma.svg" alt=",">
                <br>
                <img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/period.svg" alt=".">
            </td>
            <td>
                <p><b><a name="change_pivot_type" href="#top_change_pivot_type">Change Pivot Type</a></b></p>
                <p>
                    Changes how strips are rotated and scaled. When the Pivot Type is set to
                    "2D Cursor" you may place the cursor with the left mouse button.
                </p>
            </td>
            <td>
                <img src="https://i.imgur.com/3ru1Xl6.gif">
            </td>
            
    </table>

