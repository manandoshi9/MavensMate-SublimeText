//
//  AppDelegate.h
//
//  Created by Joseph Ferraro on 2/23/12.
//  Copyright (c) 2013 Joseph Ferraro. All rights reserved.
//


#import <Cocoa/Cocoa.h>
#import "StatusMenuController.h"

@interface AppDelegate : NSObject <NSApplicationDelegate> {

}

@property (nonatomic, retain) StatusMenuController *menuController;

@end