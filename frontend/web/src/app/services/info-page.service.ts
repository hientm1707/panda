import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { InfoPage } from '../interfaces/info-page.interface';
import { Profile } from '../interfaces/profile.interface';

@Injectable({
  providedIn: 'root'
})
export class InfoPageService {

  info: InfoPage = {};
  loaded = false;
  profile: Profile;

  constructor(private http: HttpClient) {
    this.loadInfo();
    this.loadProfile();
  }

  private loadInfo() {
    this.http.get('./assets/data/data.page.json')
      .subscribe((resp: InfoPage) => {
        this.loaded = true;
        this.info = resp;
      });
  }
  private loadProfile() {
    this.http.get('./assets/data/profile.page.json')
      .subscribe((resp: Profile) => {
        this.profile = resp;
      });
  }
}
