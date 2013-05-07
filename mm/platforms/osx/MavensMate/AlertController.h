//
//  AlertController.h
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface AlertController : NSWindowController <NSWindowDelegate> {
@private
    IBOutlet NSWindow *_alertWindow;
    IBOutlet NSTextField *alertMessage;
    IBOutlet NSButton *_alertButton;
}

@property (strong) IBOutlet NSTextField *alertMessage;

-(void)showWithMessage:(NSString*)message;
-(void)show;
-(void)hide;

@end
