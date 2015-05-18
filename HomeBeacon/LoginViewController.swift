//

import UIKit
import Accounts
import TwitterKit
import TwitterKit


class LoginViewController: UIViewController {
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        let authenticateButton = DGTAuthenticateButton(authenticationCompletion: {
            (session: DGTSession!, error: NSError!) in
            // play with Digits session
            if error != nil {
                // there was an error
            } else {
                //
                self.performSegueWithIdentifier("show", sender: self)
            }
        })
        authenticateButton.center = self.view.center
        self.view.addSubview(authenticateButton)

    }
    
}