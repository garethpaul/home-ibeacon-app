
//  ViewController.swift
//

import UIKit
import CoreLocation

class ViewController: UIViewController{
    
    
    let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
    
    @IBOutlet weak var imageLoc: UIImageView!
    var logoView: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupNav()
        findLocation()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func setupNav() {
        // SetupNav
        logoView = UIImageView(frame: CGRectMake(0, 0, 40, 40))
        logoView.image = UIImage(named: "logo")?.imageWithRenderingMode(.AlwaysTemplate)
        logoView.tintColor = toColor("121212")
        logoView.frame.origin.x = (self.view.frame.size.width - logoView.frame.size.width) / 2
        logoView.frame.origin.y = 20
        // Add the logo view to the navigation controller.
        self.navigationController?.view.addSubview(logoView)
        
        // Bring the logo view to the front.
        self.navigationController?.view.bringSubviewToFront(logoView)
        
        // Customize the navigation bar.
        self.navigationController?.navigationBar.barTintColor = toColor("FF9800")
        self.navigationController?.navigationBar.shadowImage = UIImage()
    }
    
    func findLocation() {
        let delayTime = dispatch_time(DISPATCH_TIME_NOW,
            Int64(3 * Double(NSEC_PER_SEC)))
        dispatch_after(delayTime, dispatch_get_main_queue()) {
            if (self.appDelegate.currentLocation == "home") {
                self.imageLoc.image = UIImage(named: "home.png")
            } else {
                self.imageLoc.image = UIImage(named: "out.png")
            }
        }
    }
}


