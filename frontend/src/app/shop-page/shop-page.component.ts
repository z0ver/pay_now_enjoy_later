import {Component, OnInit} from '@angular/core';
import {DealerProfile} from "../model/dealer-profile";
import {HelpButtonContent} from "./help-button/help-button-content";
import { ActivatedRoute, Router, NavigationStart } from '@angular/router';
import { DialogComponent } from '../dialog/dialog.component'
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-shop-page',
  templateUrl: './shop-page.component.html',
  styleUrls: ['./shop-page.component.css']
})
export class ShopPageComponent implements OnInit {

  shop: DealerProfile = new DealerProfile();
  buttons: Array<HelpButtonContent> = new Array<HelpButtonContent>();

  constructor(private router:Router, private activatedRoute:ActivatedRoute, public dialog: MatDialog) {
    const place = this.router.getCurrentNavigation().extras.state

    this.shop.short_description.name = place.short_description.name
    this.shop.short_description.short_information = place.short_description.short_information
    this.shop.address.place = place.address.place
    this.shop.address.number = place.address.number
    this.shop.address.postcode = place.address.postCode
  }

  ngOnInit(): void {
    //todo remove mock shit
    const mockButton = new HelpButtonContent();
    mockButton.header = "Gutschein";
    mockButton.description = "Ich moechte einen Sach- oder Geldwert-Gutschein erwerben";

    this.buttons.push(mockButton);
  }

  onHelpButtonClick(buttonContent: HelpButtonContent) {
    let dialogRef = this.dialog.open(DialogComponent, {
      width: '250px',
      data: { buttonContent: buttonContent }
    });
    dialogRef.afterClosed().subscribe((result) => {
      console.log(result)
    });
  }
}
