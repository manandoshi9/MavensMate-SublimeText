//
//  DragAndDropStatusMenuView.h
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface DragAndDropStatusMenuView : NSView <NSDraggingDestination, NSObject, NSMenuDelegate>{
@private
	NSMenu *_menu;
	BOOL _isMenuVisible;	
}

@property (strong, nonatomic) NSStatusItem* statusItem;

@end