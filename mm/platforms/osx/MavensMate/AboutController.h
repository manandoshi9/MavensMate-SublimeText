//
//  AlertController.h
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface AboutController : NSWindowController <NSWindowDelegate> {
@private
    IBOutlet NSTextField *versionNumber;
}

@property (strong) IBOutlet NSTextField *versionNumber;


@end
