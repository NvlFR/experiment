<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TodoController;
use Inertia\Inertia;

// Home route with Inertia
Route::inertia('/', 'Welcome')->name('home');

// API Routes - Todo CRUD operations
Route::prefix('api/todos')->group(function () {
    Route::post('/', [TodoController::class, 'store']);
    Route::get('/', [TodoController::class, 'index']);
    Route::put('/{todo}', [TodoController::class, 'update']);
    Route::delete('/{todo}', [TodoController::class, 'destroy']);
});
