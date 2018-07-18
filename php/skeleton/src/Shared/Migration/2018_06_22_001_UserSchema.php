<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class UserSchema extends Migration {

    public function up()
    {
        Schema::create('user', function(Blueprint $table)
        {
            $table->increments('id');
            $table->string('uuid');
            $table->string('instance');
            $table->integer('profile_id');
            $table->string('mail');
            $table->string('password');
            $table->integer('created');
            $table->integer('access');
            $table->integer('login');
            $table->integer('status');
            $table->string('first_name');
            $table->string('last_name');
            $table->integer('allow_public');
            $table->text('data');
            $table->integer('timestamp');
        });
    }

    public function down()
    {
        Schema::drop('user');
    }
}