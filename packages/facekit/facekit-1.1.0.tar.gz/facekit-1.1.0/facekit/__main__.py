import click
from facekit.detectors import MTCNNDetector
from vidsnap.utils import run_video_extractor


@click.group()
def main():
    click.echo("Facekit v1.1.0")


@main.command()
@click.option('--in_path', '-i', type=str, default='./in', help="Path where detector will pick up images.")
@click.option('--out_path', '-o', type=str, default='./out', help="Path where detector will store images.")
@click.option('--accuracy', '-a', type=float, default=0.98, help="Minimum detector threshold accuracy.")
@click.option('--preload', is_flag=True, help="Preload images in memory. "
                                              "More memory intensive, might be faster on HDDs!")
def extract_faces(in_path, out_path, accuracy, preload):
    detector = MTCNNDetector(input_path=in_path, output_path=out_path, accuracy_threshold=accuracy, preload=preload)
    detector.extract_faces()
    detector.store_extracted_faces()


@main.command()
@click.option('--video_in', '-v', type=str, default='./video_in')
@click.option('--video_interval', type=int, default=5)
@click.option('--detector_in', '-i', type=str, default='./detector_in')
@click.option('--detector_out', '-o', type=str, default='./detector_out')
@click.option('--accuracy', '-a', type=float, default=0.98, help="Minimum detector threshold accuracy.")
@click.option('--preload', is_flag=True, help="Preload images in memory. "
                                              "More memory intensive, might be faster on HDDs!")
def extract_faces_video(video_in, video_interval, detector_in, detector_out, accuracy, preload):
    click.secho("Running video extractor, this may take a while...")
    run_video_extractor(input_path=video_in,
                        output_path=detector_in,
                        video_extension='mp4',
                        workers=1,
                        snap_every_x=video_interval)

    detector = MTCNNDetector(input_path=detector_in, output_path=detector_out, accuracy_threshold=accuracy, preload=preload)
    detector.extract_faces()
    detector.store_extracted_faces()


if __name__ == '__main__':
    main()