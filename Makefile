devsetup:
	@uv sync

build: devsetup clean
	@uv run nuitka --onefile --output-file=xum --output-dir=build main.py 
	@mkdir -p dist
	@cp build/xum dist/xum

install:
	@cp -f build/xum ~/.local/bin/xum

clean:
	@rm -rf main.bin
	@rm -rf main.dist
	@rm -rf build
	@rm -rf dist
