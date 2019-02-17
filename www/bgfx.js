/*
	click to clear and change hue

	don't look at or judge this code
	I just kept tweaking values and
	adding random things in a messy way
	
	it's full of magic numbers
*/

var c,
	ctx,
	w,
	h,
	cx,
	cy,
	branches,
	startHue,
	tick;

function rand( min, max ) {
	return Math.random() * ( max - min ) + min;
}

function randInt( min, max ) {
	return Math.floor( min + Math.random() * ( max - min + 1 ) );
};

function Branch( hue, x, y, angle, vel ) {
	var move = 250;
	this.x = x + rand( -move, move );
	this.y = y + rand( -move, move );
	this.points = [];
	this.angle = angle != undefined ? angle : rand( 0, Math.PI * 1 );
	this.vel = vel != undefined ? vel : rand( -4, 4 );
	this.spread = 0;
	this.tick = 0;
	this.hue = hue != undefined ? hue : 200;
	this.life = 1;
	this.decay = 0.0025;
	this.dead = false;
	
	this.points.push({
		x: this.x,
		y: this.y
	});
}

Branch.prototype.step = function( i ) {
	this.life -= this.decay;
	if( this.life <= 0 ) {
		this.dead = true;	
	}
	
	if( !this.dead ) {
		var lastPoint = this.points[ this.points.length - 1 ];
		this.points.push({
			x: lastPoint.x + Math.cos( this.angle ) * this.vel,
			y: lastPoint.y + Math.sin( this.angle ) * this.vel
		});
		this.angle += rand( -this.spread, this.spread );
		this.vel *= 0.999;
		this.spread = this.vel * 0.05;
		this.tick++;
		this.hue += 0.3;
	} else {
		branches.splice( i, 1 );
	}
};

Branch.prototype.draw = function() {
	if( !this.points.length || this.dead ) {
		return false;
	}
	
	var length = this.points.length,
		i = length - 1,
		point = this.points[ i ],
		lastPoint = this.points[ i - randInt( 5, 100 ) ];
		//jitter = 8;
	if( lastPoint ) {
		var jitter = 2 + this.life * 6;
		ctx.beginPath();
		ctx.moveTo( lastPoint.x, lastPoint.y );
		ctx.lineTo( point.x + rand( -jitter, jitter ), point.y + rand( -jitter, jitter ) );
		ctx.lineWidth = 1;
		var alpha = this.life * 0.075;
		ctx.strokeStyle = 'hsla(' + ( this.hue + rand( -10, 10 ) ) + ', 70%, 40%, ' + alpha + ')';
		ctx.stroke();
	}
}

function init() {
	$('#logo').hide(() => {
		$('#logo').delay(2000).fadeIn("slow", () => {});
	});

	$('#instruction').hide(() => {
		$('#instruction').delay(2750).fadeIn("fast", () => {});
	});

	c = document.getElementById( 'c' );
	ctx = c.getContext( '2d' );
	startHue = 290;//220;
	branches = [];
	reset();
	loop();
}

function reset() {
	w = window.innerWidth-10;
	h = window.innerHeight-4;
	cx = w / 2;
	cy = h / 2;
	branches.length = 0;
	c.width = w;
	c.height = h;
	tick = 0;
	
	
	/*for( var i = 0; i < 125; i++ ) {		
		branches.push( new Branch( startHue, cx, cy) );
	}*/

	for( var i = 0; i < 100; i++ ) {		
		branches.push( new Branch( startHue, cx, cy) );
		branches.push( new Branch( startHue-80, cx, cy) );
	}
}

function step() {
	var i = branches.length;
	while( i-- ) { branches[ i ].step( i ) }
	tick++;
}

function draw() {
	var i = branches.length;
	if( tick < 450 ) {
		ctx.save();
		ctx.globalCompositeOperation = 'lighter';
		ctx.globalAlpha = 0.002;
		ctx.translate( cx, cy );
		var scale = 1 + tick * 0.0025 ;
		ctx.scale( scale, scale );
		ctx.translate( -cx, -cy );
		ctx.drawImage( c, rand( -150, 150 ), rand( -150, 150 ) );
		ctx.restore();
	}
	
	ctx.globalCompositeOperation = 'lighter';
		while( i-- ) { branches[ i ].draw() }
}

function loop() {
	requestAnimationFrame( loop );
	step();
	draw();
	step();
	draw();
}

window.addEventListener( 'resize', reset );
/*window.addEventListener( 'click', function() {
	startHue += 60;
	reset();
});*/
window.onload = function () { init(); }
//init();
