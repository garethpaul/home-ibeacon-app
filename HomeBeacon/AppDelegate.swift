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

    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        // Override point for customization after application launch.
        Fabric.with([Twitter()])
        
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
        beaconRegion.notifyOnEntry = true
        beaconRegion.notifyOnExit = true
        //beaconRegion.notifyEntryStateOnDisplay = true
        locationManager!.startMonitoringForRegion(beaconRegion)
        
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
    func locationManager(manager: CLLocationManager!,
        didRangeBeacons beacons: [AnyObject]!,
        inRegion region: CLBeaconRegion!) {
            
            //NSLog("didRangeBeacons");
            if(beacons != nil && beacons.count > 0) {
                if let nearestBeacon = beacons[0] as? CLBeacon {
                    if(nearestBeacon.proximity == lastProximity ||
                        nearestBeacon.proximity == CLProximity.Unknown) {
                        return;
                    }
                    lastProximity = nearestBeacon.proximity;
                } else {
                    return;
                }
            } else {
                
                if(lastProximity == CLProximity.Unknown) {
                    return;
                }
                
                lastProximity = CLProximity.Unknown
            }
            
            // Location-state logging is intentionally disabled to avoid
            // recording home/away presence in device logs.
    }
    
    func locationManager(manager: CLLocationManager!,
        didEnterRegion region: CLRegion!) {
            if let beaconRegion = region as? CLBeaconRegion {
                manager.startRangingBeaconsInRegion(beaconRegion)
            }
            
            // Location-state logging is intentionally disabled to avoid
            // recording home/away presence in device logs.
            // Network reporting is intentionally disabled until endpoint,
            // payload consent, and retention behavior are documented.
    }
    
    func locationManager(manager: CLLocationManager!,
        didExitRegion region: CLRegion!) {
            if let beaconRegion = region as? CLBeaconRegion {
                manager.stopRangingBeaconsInRegion(beaconRegion)
                lastProximity = nil
            }
            
            // Location-state logging is intentionally disabled to avoid
            // recording home/away presence in device logs.
            // Network reporting is intentionally disabled until endpoint,
            // payload consent, and retention behavior are documented.
    }
}
