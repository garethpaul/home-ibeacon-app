
//  ViewController.swift
//

import UIKit
import CoreLocation

class ViewController: UIViewController{
    
    
    let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
    
    @IBOutlet weak var imageLoc: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        println("get location")
        println(appDelegate.currentLocation)
        
        let delayTime = dispatch_time(DISPATCH_TIME_NOW,
            Int64(3 * Double(NSEC_PER_SEC)))
        dispatch_after(delayTime, dispatch_get_main_queue()) {
            if (self.appDelegate.currentLocation == "home") {
                self.imageLoc.image = UIImage(named: "home.png")
            }
        }
    
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}


