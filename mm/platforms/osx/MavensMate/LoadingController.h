//
//  LoadingController.h
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface LoadingController : NSWindowController <NSWindowDelegate> {
@private
    IBOutlet NSWindow *_loadingWindow;
    IBOutlet NSProgressIndicator *_loadingBar;
}

-(void)show;
-(void)hide;

@end
