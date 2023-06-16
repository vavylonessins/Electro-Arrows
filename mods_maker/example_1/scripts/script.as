alias neonscript as neon;

neon::script {

    example: function {
        neon::io::print("Test");
    }
};

neon::main {

    types {

        button {

            dirs 1;

            states (charge,);

        };
    }

    textures {

        button {

            png "button_u.png";
            vec "button_u.vec";
        
        };

        button charge {

            png "button_c.png";
            vec "button_c.vec";

        };

    };

    behavior {

        for button {

            neon::events::OnMouseButtonPress {

                neon::api::showNotifyPopup("Button was pressed!");
                neon::api::setState(this, charge);
        
            };

            neon::events::OnMouseButtonRelease {

                neon::api::showNotifyPopup("Button was released!");
                neon::api::clearState(this, charge);
        
            };
        
        };

    };

};
