//

import UIKit
import TwitterKit

class LoginViewController: UIViewController {
    
    @IBOutlet weak var loginBtn: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        Digits.sharedInstance().logOut()
        loginBtn.layer.cornerRadius = 5
        loginBtn.layer.borderWidth = 1
        loginBtn.layer.borderColor = UIColor.clearColor().CGColor
    }
    
    @IBAction func didTap(sender: AnyObject) {
        let digits = Digits.sharedInstance()
        digits.authenticateWithCompletion { (session, error) in
            print("hi")
            print(session.phoneNumber)
            // Inspect session/error objects
            if error != nil {
                // there was an error
                println("error")
            } else {
                //
                self.performSegueWithIdentifier("show", sender: self)
            }
        }
        
    }
    
}