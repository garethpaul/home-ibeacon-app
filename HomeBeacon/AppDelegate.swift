//
//  AppDelegate.swift
//  HomeBeacon
//

import UIKit
import CoreLocation
import Alamofire
import Fabric
import TwitterKit


@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate, CLLocationManagerDelegate {
    

    var window: UIWindow?
    var locationManager: CLLocationManager?
    var lastProximity: CLProximity?
    var currentLocation: String?

    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        // Override point for customization after application launch.
        Fabric.with([Twitter()])
        
        if(UIApplication.instancesRespondToSelector(Selector("registerUserNotificationSettings:"))) {
            UIApplication.sharedApplication().registerUserNotificationSettings(UIUserNotificationSettings(forTypes: .Sound | .Alert | .Badge, categories: nil))
        }

        let uuidString = "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6"
        let beaconIdentifier = "iBeaconModules.us"
        let beaconUUID:NSUUID = NSUUID(UUIDString: uuidString)!
        let beaconRegion:CLBeaconRegion = CLBeaconRegion(proximityUUID: beaconUUID,
            identifier: beaconIdentifier)
        
        locationManager = CLLocationManager()
        if(locationManager!.respondsToSelector("requestAlwaysAuthorization")) {
            locationManager!.requestAlwaysAuthorization()
        }
        
        locationManager!.delegate = self
        locationManager!.pausesLocationUpdatesAutomatically = false
        beaconRegion.notifyOnEntry = true
        beaconRegion.notifyOnExit = true
        //beaconRegion.notifyEntryStateOnDisplay = true
        locationManager!.startMonitoringForRegion(beaconRegion)
        locationManager!.startRangingBeaconsInRegion(beaconRegion)
        locationManager!.startUpdatingLocation()
        
        if Digits.sharedInstance().session() == nil {
            let storyboard = UIStoryboard(name: "Main", bundle: nil)
            let authViewController: AnyObject! = storyboard.instantiateViewControllerWithIdentifier("LoginViewController")
            self.window?.rootViewController = authViewController as? UIViewController
        }

        return true
        
    }

    func applicationWillResignActive(application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }
}

extension AppDelegate: CLLocationManagerDelegate {
    func sendLocalNotificationWithMessage(message: String!, playSound: Bool) {
        let notification:UILocalNotification = UILocalNotification()
        notification.alertBody = message
        
        if(playSound) {
            notification.soundName = "tos_beep.caf";
        }
        
        UIApplication.sharedApplication().scheduleLocalNotification(notification)
    }
    
    func locationManager(manager: CLLocationManager!,
        didRangeBeacons beacons: [AnyObject]!,
        inRegion region: CLBeaconRegion!) {
            
            //NSLog("didRangeBeacons");
            var message:String = ""
            
            var playSound = false
            
            if(beacons.count > 0) {
                let nearestBeacon:CLBeacon = beacons[0]as! CLBeacon
                
                if(nearestBeacon.proximity == lastProximity ||
                    nearestBeacon.proximity == CLProximity.Unknown) {
                        return;
                }
                lastProximity = nearestBeacon.proximity;
                
                switch nearestBeacon.proximity {
                case CLProximity.Far:
                    message = "You are far away from the beacon"
                    self.currentLocation = "home" 
                    playSound = true
                case CLProximity.Near:
                    message = "You are near the beacon"
                    self.currentLocation = "home"
                case CLProximity.Immediate:
                    message = "You are in the immediate proximity of the beacon"
                    self.currentLocation = "home"
                case CLProximity.Unknown:
                    return
                }
            } else {
                
                if(lastProximity == CLProximity.Unknown) {
                    return;
                }
                
                message = "No beacons are nearby"
                playSound = true
                lastProximity = CLProximity.Unknown
            }
            
            NSLog("%@", message)
            //sendLocalNotificationWithMessage(message, playSound: playSound)
    }
    
    func locationManager(manager: CLLocationManager!,
        didEnterRegion region: CLRegion!) {
            manager.startRangingBeaconsInRegion(region as! CLBeaconRegion)
            manager.startUpdatingLocation()
            
            if Digits.sharedInstance().session() != nil {
                var session = Digits.sharedInstance().session()
                let parameters = [
                    "phoneNumber": session.phoneNumber,
                    "userId": session.userID,
                    "msg": "came home"
                ]
                self.currentLocation = "home"                
                //Alamofire.request(.POST, "https://requestlabs.appspot.com/whine/beacon", parameters: parameters)
                
            }
            
            NSLog("You entered the region")
            
            //sendLocalNotificationWithMessage("You entered the region", playSound: false)
    }
    
    func locationManager(manager: CLLocationManager!,
        didExitRegion region: CLRegion!) {
            manager.stopRangingBeaconsInRegion(region as! CLBeaconRegion)
            manager.stopUpdatingLocation()
            
            if Digits.sharedInstance().session() != nil {
                var session = Digits.sharedInstance().session()
                let parameters = [
                    "phoneNumber": session.phoneNumber,
                    "userId": session.userID,
                    "msg": "left home"
                ]
                self.currentLocation = "not home"
                
                //Alamofire.request(.POST, "https://requestlabs.appspot.com/whine/beacon", parameters: parameters)
                
            }
            
            
            NSLog("You exited the region")
            //sendLocalNotificationWithMessage("You exited the region", playSound: true)
    }
}


