import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';

let log = console.log;
let error = console.error;

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}
const apiUrl = 'https://jsonplaceholder.typicode.com/albums';

@Component({
  selector: 'app-api',
  imports: [
    CommonModule
  ],
  templateUrl: './api.component.html',
  styleUrl: './api.component.scss'
})
export class ApiComponent implements OnInit {

  albums: any[] = []

  constructor(private http: HttpClient) {

    this.getAlbums().subscribe( (res: any) => {
      this.albums = res
      log( this.albums )
    }, err => {
      error(err)
    }
    )

  }

  ngOnInit() {

    setTimeout(() => {
      this.searchAlbumsByTitle('omni')
    }, 4000)

  }

  private handleError<T> (operation='operation', result?: T) {
    return (error: any): Observable<T> => {
      error(error)
      return of(result as T)
    };
  }

  getAlbums(): Observable<any[]> {
    return this.http.get<any[]>(apiUrl).pipe(
      tap( albums => log('fetched albums'), catchError( this.handleError('getAlbums', [])) )
    );
  }

  getAlbumById(id: number): Observable<any[]> {
    return this.http.get<any[]>(`${apiUrl}/${id}`).pipe(
      tap( albums => log(`fetched album ${id}`), catchError( this.handleError('getAlbums', [])) )
    );
  }

  searchAlbumsByTitle(title: string) {
    let sAlbums = []
    for ( let id in this.albums )
    {
      //log(this.albums[id])
      //log(typeof album)

      //if (title in this.albums[id].title)

      if (this.albums[id].title.includes(title))
        sAlbums.push(this.albums[id])
    }
    log(sAlbums)
    this.albums = sAlbums
  }

}
