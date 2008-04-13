""" A TVTK scene editor. """

# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Enthought, Inc.
# License: BSD Style.


# Enthought library imports.
from enthought.preferences.api import bind_preference
from enthought.pyface.tvtk.scene import Scene
from enthought.pyface.workbench.api import Editor
from enthought.traits.api import Instance


#### Handy functions ##########################################################

def _id_generator():
    """ Return an ever-increasing number useful for creating unique Ids. """

    n = 1
    while True:
        yield(n)
        n += 1

_id_generator = _id_generator()


class SceneEditor(Editor):
    """ A TVTK scene editor. """

    #### 'SceneEditor' interface ##############################################
    
    # The TVTK scene object.
    scene = Instance(Scene)

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def _id_default(self):
        """ Trait initializer. """

        return self.name

    def _name_default(self):
        """ Trait initializer. """

        return 'TVTK Scene %d' % (_id_generator.next())

    #### Methods ##############################################################
    
    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor. """

        # We hold a reference to the scene itself to make sure it does not get
        # garbage collected (because we only return the scene's 'control' not
        # the scene itself). The scene is also referenced by the scene manager.
        self.scene = self._create_decorated_scene(parent)
        self.scene.render()

        return self.scene.control

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_decorated_scene(self, parent):
        """ Create a new decorated scene. """

        # fixme: This should be 'DecoratedScene' but I couldn't get that to
        # work! It barfed saying the wx backend doesn't implement it...
        scene = Scene(parent)

        # Bind the scene's traits to preferences.
        bind_preference(
            scene, 'stereo', 'enthought.tvtk.scene.stereo'
        )

        bind_preference(
            scene, 'magnification', 'enthought.tvtk.scene.magnification'
        )

        bind_preference(
           scene, 'foreground', 'enthought.tvtk.scene.foreground_color'
        )

        # fixme: This preference is bound to the renderer not the scene! Why
        # doesn't the scene expose this trait too (especially since it exposes
        # the foreground colour!)?
        bind_preference(
            scene.renderer,'background','enthought.tvtk.scene.background_color'
        )

        return scene
        
#### EOF ######################################################################
